'use strict';

const required = [
  {
    name: 'DATABASE_URL',
    hint: 'Postgres/Neon connection string for the dashboard API.',
  },
  {
    name: 'IDEATE_DASHBOARD_ADMIN_TOKEN',
    hint: 'Admin token expected by protected dashboard API routes.',
  },
];

const missing = required.filter((item) => !process.env[item.name]);

if (missing.length) {
  console.error('Dashboard API environment is not configured.');
  console.error('');
  for (const item of missing) {
    console.error(`Missing ${item.name}: ${item.hint}`);
  }
  console.error('');
  console.error('Export these variables in the same terminal before starting the dashboard:');
  console.error('');
  console.error('  export DATABASE_URL="<postgres-connection-string>"');
  console.error('  export IDEATE_DASHBOARD_ADMIN_TOKEN="<choose-a-local-token>"');
  console.error('  npm run start:vercel');
  console.error('');
  console.error('Then paste the same admin token into the dashboard token field.');
  process.exit(1);
}
