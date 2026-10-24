import {readFileSync, writeFileSync} from 'node:fs';
const [team, audience] = process.argv.slice(2);
if (!team || !/^[a-z0-9-]+\.cloudflareaccess\.com$/.test(team) || !audience || !/^[a-zA-Z0-9_-]{16,256}$/.test(audience)) {
  console.error('Usage: npm run cloud:access:configure -- TEAM.cloudflareaccess.com APPLICATION_AUD');
  process.exitCode = 1;
} else {
  const path = new URL('../cloud/gateway/wrangler.jsonc', import.meta.url);
  const config = JSON.parse(readFileSync(path, 'utf8'));
  config.vars.ACCESS_TEAM_DOMAIN = team;
  config.vars.ACCESS_AUD = audience;
  writeFileSync(path, JSON.stringify(config, null, 2) + '\n');
  console.log('Saved non-secret Access identifiers. Verify the exact email policy, generate types, test and redeploy the gateway.');
}
