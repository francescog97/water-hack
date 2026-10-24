import {authenticatedEmail} from './auth.ts';

const CSP = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'";

function secure(response: Response): Response {
  const result = new Response(response.body, response);
  result.headers.set('Cache-Control', 'no-store');
  result.headers.set('X-Content-Type-Options', 'nosniff');
  result.headers.set('Referrer-Policy', 'no-referrer');
  result.headers.set('Content-Security-Policy', CSP);
  return result;
}

function error(detail: string, status: number) {
  return secure(Response.json({detail}, {status}));
}

async function boundedBody(request: Request): Promise<Uint8Array | undefined> {
  if (!request.body) return undefined;
  const reader = request.body.getReader();
  const parts: Uint8Array[] = [];
  let length = 0;
  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    length += value.length;
    if (length > 65536) { await reader.cancel(); throw new RangeError('Request too large'); }
    parts.push(value);
  }
  const body = new Uint8Array(length);
  let offset = 0;
  for (const part of parts) { body.set(part, offset); offset += part.length; }
  return body;
}

export async function handle(request: Request, env: Env, verify = authenticatedEmail): Promise<Response> {
  const url = new URL(request.url);
  if (url.origin !== env.PUBLIC_ORIGIN) return error('Unknown application host', 403);
  if (!env.ACCESS_TEAM_DOMAIN || !env.ACCESS_AUD) return error('Private application: login configuration pending', 503);
  let email: string;
  try { email = await verify(request, env); }
  catch { return error('Sign in with an authorized email through Cloudflare Access', 401); }

  if (!['GET', 'HEAD', 'POST', 'OPTIONS'].includes(request.method)) return error('Method not allowed', 405);
  const origin = request.headers.get('Origin');
  if (!['GET', 'HEAD', 'OPTIONS'].includes(request.method) && origin && origin !== env.PUBLIC_ORIGIN) {
    return error('Cross-origin writes are disabled', 403);
  }
  if (url.pathname === '/api/session') return secure(Response.json({email, mode: 'private-cloud-historical-demo'}));
  if (url.pathname.startsWith('/api/')) {
    let body: Uint8Array | undefined;
    try { body = await boundedBody(request); }
    catch { return error('Request body too large', 413); }
    const headers = new Headers();
    headers.set('Host', 'crisis2action-api.internal');
    headers.set('x-c2a-user-email', email);
    if (origin) headers.set('Origin', origin);
    if (request.headers.has('Content-Type')) headers.set('Content-Type', request.headers.get('Content-Type')!);
    try {
      const upstream = await env.BACKEND.fetch(new Request(`https://crisis2action-api.internal${url.pathname}${url.search}`, {
        method: request.method, headers, body,
      }));
      return secure(upstream);
    } catch {
      console.error(JSON.stringify({event: 'backend_unavailable'}));
      return error('Backend unavailable. No replacement observation has been invented.', 503);
    }
  }
  if (!['GET', 'HEAD'].includes(request.method)) return error('Not found', 404);
  if (url.pathname !== '/' && url.pathname !== '/index.html' && !/^\/assets\/[a-zA-Z0-9_./-]+\.(js|css|svg|png|ico|woff2?)$/.test(url.pathname)) {
    return error('Not found', 404);
  }
  return secure(await env.ASSETS.fetch(request));
}

export default {fetch: (request, env) => handle(request, env)} satisfies ExportedHandler<Env>;
