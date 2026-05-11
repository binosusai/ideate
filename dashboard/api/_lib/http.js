'use strict';

const SAFE_STATUS_CODES = new Set([400, 401, 403, 404, 405, 409, 422, 500, 502, 503]);

class HttpError extends Error {
  constructor(statusCode, message, code = 'request_failed') {
    super(message);
    this.name = 'HttpError';
    this.statusCode = SAFE_STATUS_CODES.has(statusCode) ? statusCode : 500;
    this.code = code;
  }
}

function methodNotAllowed(res, allowedMethods) {
  res.setHeader('Allow', allowedMethods.join(', '));
  res.status(405).json({ error: 'Method not allowed', code: 'method_not_allowed' });
}

function sendError(res, error) {
  if (error instanceof HttpError) {
    res.status(error.statusCode).json({ error: error.message, code: error.code });
    return;
  }

  console.error('[dashboard-api] unexpected error', {
    name: error && error.name ? error.name : 'Error',
    message: error && error.message ? sanitizeErrorMessage(error.message) : 'Unknown error',
  });
  res.status(500).json({ error: 'Unexpected dashboard API error.', code: 'internal_error' });
}

function sanitizeErrorMessage(message) {
  return String(message)
    .replace(/postgres(?:ql)?:\/\/[^\s'"]+/gi, '[redacted-database-url]')
    .replace(/password=[^\s'"]+/gi, 'password=[redacted]');
}

module.exports = {
  HttpError,
  methodNotAllowed,
  sendError,
};
