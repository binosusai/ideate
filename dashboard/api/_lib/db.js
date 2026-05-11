'use strict';

const { HttpError } = require('./http');

let pool;

function getPool() {
  const connectionString = process.env.DATABASE_URL || '';
  if (!connectionString) {
    throw new HttpError(503, 'Dashboard database is not configured.', 'database_not_configured');
  }

  if (!pool) {
    const { Pool } = require('pg');
    pool = new Pool({
      connectionString,
      max: Number(process.env.IDEATE_DASHBOARD_DB_POOL_MAX || 3),
      idleTimeoutMillis: 10_000,
      connectionTimeoutMillis: 8_000,
      ssl: connectionString.includes('sslmode=require') ? { rejectUnauthorized: false } : undefined,
    });
  }
  return pool;
}

async function query(sql, params = []) {
  try {
    return await getPool().query(sql, params);
  } catch (error) {
    console.error('[dashboard-api] database query failed', {
      code: error && error.code ? error.code : 'unknown',
      routine: error && error.routine ? error.routine : undefined,
    });
    throw new HttpError(502, 'Dashboard database query failed.', 'database_query_failed');
  }
}

async function withTransaction(work) {
  const client = await getPool().connect();
  try {
    await client.query('BEGIN');
    const result = await work({
      query: (sql, params = []) => client.query(sql, params),
    });
    await client.query('COMMIT');
    return result;
  } catch (error) {
    try {
      await client.query('ROLLBACK');
    } catch (rollbackError) {
      console.error('[dashboard-api] rollback failed', {
        code: rollbackError && rollbackError.code ? rollbackError.code : 'unknown',
      });
    }
    if (error instanceof HttpError) {
      throw error;
    }
    console.error('[dashboard-api] transaction failed', {
      code: error && error.code ? error.code : 'unknown',
      routine: error && error.routine ? error.routine : undefined,
    });
    throw new HttpError(502, 'Dashboard database transaction failed.', 'database_transaction_failed');
  } finally {
    client.release();
  }
}

function compactIdea(row) {
  if (!row) return null;
  const details = row.details_json && typeof row.details_json === 'object' ? row.details_json : {};
  return {
    id: row.id,
    title: row.title,
    slug: row.slug,
    category: row.category,
    status: row.status,
    score: Number(row.score || 0),
    review_status: row.review_status || 'new',
    tinkered: Boolean(row.tinkered),
    hardened: Boolean(row.hardened),
    iteration_count: Number(row.iteration_count || 0),
    created_at: row.created_at,
    updated_at: row.updated_at,
    domain: details.domain || '',
    source_category: details.source_category || '',
    target_users: Array.isArray(details.target_users) ? details.target_users.slice(0, 4) : [],
  };
}

async function listIdeas({ status = '', reviewStatus = '', q = '', limit = 50 } = {}) {
  const clauses = [];
  const params = [];

  if (status) {
    params.push(status);
    clauses.push(`status = $${params.length}`);
  }
  if (reviewStatus) {
    params.push(reviewStatus);
    clauses.push(`review_status = $${params.length}`);
  }
  if (q) {
    params.push(`%${q}%`);
    clauses.push(`(title ILIKE $${params.length} OR slug ILIKE $${params.length})`);
  }

  const safeLimit = Math.max(1, Math.min(Number(limit) || 50, 100));
  params.push(safeLimit);
  const where = clauses.length ? `WHERE ${clauses.join(' AND ')}` : '';
  const result = await query(
    `
    SELECT id, title, slug, category, status, score, review_status, tinkered, hardened,
           iteration_count, created_at, updated_at, details_json
    FROM ideas
    ${where}
    ORDER BY
      CASE category WHEN 'money' THEN 0 ELSE 1 END,
      score DESC,
      updated_at DESC
    LIMIT $${params.length}
    `,
    params,
  );
  return result.rows.map(compactIdea);
}

async function getIdeaById(ideaId, db = { query }) {
  const result = await db.query('SELECT * FROM ideas WHERE id = $1', [ideaId]);
  return result.rows[0] || null;
}

async function latestArtifacts(ideaId, kinds, db = { query }) {
  if (!Array.isArray(kinds) || kinds.length === 0) return {};
  const result = await db.query(
    `
    SELECT DISTINCT ON (kind) kind, content, created_at
    FROM artifacts
    WHERE idea_id = $1 AND kind = ANY($2::text[])
    ORDER BY kind, created_at DESC, id DESC
    `,
    [ideaId, kinds],
  );
  return Object.fromEntries(result.rows.map((row) => [row.kind, { content: row.content, created_at: row.created_at }]));
}

async function recentDecisions(ideaId, limit = 10, db = { query }) {
  const safeLimit = Math.max(1, Math.min(Number(limit) || 10, 50));
  const result = await db.query(
    `
    SELECT id, decision, rationale, created_at
    FROM decisions
    WHERE idea_id = $1
    ORDER BY created_at DESC, id DESC
    LIMIT $2
    `,
    [ideaId, safeLimit],
  );
  return result.rows;
}

function notFoundIfMissing(row, ideaId) {
  if (!row) {
    throw new HttpError(404, `Idea ${ideaId} was not found.`, 'idea_not_found');
  }
}

async function addDecision(db, ideaId, decision, rationale) {
  await db.query(
    'INSERT INTO decisions(idea_id, decision, rationale) VALUES ($1, $2, $3)',
    [ideaId, decision, String(rationale || '').trim()],
  );
}

async function approveIdea(ideaId, rationale = '') {
  return withTransaction(async (db) => {
    const current = await getIdeaById(ideaId, db);
    notFoundIfMissing(current, ideaId);

    if (current.status === 'approved') {
      return { idea: current, changed: false };
    }
    if (current.status !== 'planned') {
      throw new HttpError(409, 'Only planned ideas can be approved from the dashboard.', 'invalid_approval_transition');
    }

    const result = await db.query(
      `
      UPDATE ideas
      SET status = 'approved', updated_at = NOW()
      WHERE id = $1
      RETURNING *
      `,
      [ideaId],
    );
    const updated = result.rows[0];
    await addDecision(db, ideaId, 'dashboard-approved', rationale || 'Approved from dashboard.');
    return { idea: updated, changed: true };
  });
}

async function reviewIdea(ideaId, decision, feedback = '') {
  const normalizedDecision = String(decision || '').trim();
  if (!['approve', 'revise'].includes(normalizedDecision)) {
    throw new HttpError(422, 'Review decision must be approve or revise.', 'invalid_review_decision');
  }

  return withTransaction(async (db) => {
    const current = await getIdeaById(ideaId, db);
    notFoundIfMissing(current, ideaId);

    if (normalizedDecision === 'approve' && current.review_status === 'approved') {
      return { idea: current, changed: false };
    }
    if (normalizedDecision === 'revise' && current.review_status === 'revise' && String(current.review_feedback || '') === String(feedback || '').trim()) {
      return { idea: current, changed: false };
    }
    if (current.review_status !== 'pending_review') {
      throw new HttpError(409, 'Only pending POC reviews can be changed from the dashboard.', 'invalid_review_transition');
    }

    if (normalizedDecision === 'approve') {
      const result = await db.query(
        `
        UPDATE ideas
        SET review_status = 'approved',
            review_feedback = $2,
            tinkered = TRUE,
            last_reviewed_at = NOW(),
            updated_at = NOW()
        WHERE id = $1
        RETURNING *
        `,
        [ideaId, String(feedback || '').trim()],
      );
      const updated = result.rows[0];
      await addDecision(db, ideaId, 'dashboard-poc-approved', feedback || 'POC approved from dashboard.');
      return { idea: updated, changed: true };
    }

    const note = String(feedback || 'POC needs another iteration.').trim();
    const result = await db.query(
      `
      UPDATE ideas
      SET review_status = 'revise',
          review_feedback = $2,
          tinkered = FALSE,
          last_reviewed_at = NOW(),
          updated_at = NOW()
      WHERE id = $1
      RETURNING *
      `,
      [ideaId, note],
    );
    const updated = result.rows[0];
    await addDecision(db, ideaId, 'dashboard-poc-revise', note);
    return { idea: updated, changed: true };
  });
}

module.exports = {
  approveIdea,
  compactIdea,
  getIdeaById,
  latestArtifacts,
  listIdeas,
  query,
  recentDecisions,
  reviewIdea,
  withTransaction,
};
