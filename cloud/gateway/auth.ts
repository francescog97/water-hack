import {createRemoteJWKSet, jwtVerify, type JWTVerifyGetKey} from 'jose';

type AuthSettings = Pick<Env, 'ACCESS_TEAM_DOMAIN' | 'ACCESS_AUD' | 'ALLOWED_EMAILS'>;
const keySets = new Map<string, JWTVerifyGetKey>();

export async function authenticatedEmail(request: Request, env: AuthSettings, testKeys?: JWTVerifyGetKey): Promise<string> {
  if (!/^[a-z0-9-]+\.cloudflareaccess\.com$/.test(env.ACCESS_TEAM_DOMAIN) || !env.ACCESS_AUD) {
    throw new Error('Access is not configured');
  }
  const token = request.headers.get('Cf-Access-Jwt-Assertion');
  if (!token || token.length > 16384) throw new Error('Authentication required');
  const issuer = `https://${env.ACCESS_TEAM_DOMAIN}`;
  let keys = testKeys ?? keySets.get(issuer);
  if (!keys) {
    keys = createRemoteJWKSet(new URL(`${issuer}/cdn-cgi/access/certs`), {timeoutDuration: 5000});
    // Configuration is fixed per deployment; no request-specific state is cached.
    keySets.set(issuer, keys);
  }
  const {payload} = await jwtVerify(token, keys, {
    issuer, audience: env.ACCESS_AUD, algorithms: ['RS256'],
    requiredClaims: ['iss', 'aud', 'exp', 'iat', 'sub', 'email'], clockTolerance: 5,
  });
  const email = typeof payload.email === 'string' ? payload.email.toLowerCase() : '';
  const allowed = env.ALLOWED_EMAILS.split(',').map(value => value.trim().toLowerCase()).filter(Boolean);
  if (!email || !allowed.includes(email)) throw new Error('Email is not authorized');
  return email;
}
