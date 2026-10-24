import test from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPair, SignJWT, createLocalJWKSet, exportJWK} from 'jose';
import {authenticatedEmail} from '../../cloud/gateway/auth.ts';
import {handle} from '../../cloud/gateway/index.ts';

const origin = 'https://crisis2action.spunto-speak.workers.dev';
const email = 'francescogabrielg@gmail.com';
const settings = {ACCESS_TEAM_DOMAIN: 'test-team.cloudflareaccess.com', ACCESS_AUD: 'app-audience', ALLOWED_EMAILS: email};
const {privateKey, publicKey} = await generateKeyPair('RS256');
const key = await exportJWK(publicKey);
key.kid = 'test-key';
const keys = createLocalJWKSet({keys: [key]});

async function token(overrides = {}, signingKey = privateKey) {
  return new SignJWT({email, ...overrides}).setProtectedHeader({alg: 'RS256', kid: 'test-key'})
    .setIssuer('https://test-team.cloudflareaccess.com').setAudience('app-audience')
    .setSubject('reviewer-1').setIssuedAt().setExpirationTime('5m').sign(signingKey);
}

test('only a valid signed Access identity with exact audience and allowed email is accepted', async () => {
  const good = await token();
  assert.equal(await authenticatedEmail(new Request(origin, {headers: {'Cf-Access-Jwt-Assertion': good}}), settings, keys), email);
  const forged = new Request(origin, {headers: {'Cf-Access-Jwt-Assertion': good.slice(0, -10) + 'tampered00'}});
  await assert.rejects(authenticatedEmail(forged, settings, keys));
  await assert.rejects(authenticatedEmail(new Request(origin), settings, keys));
  await assert.rejects(authenticatedEmail(new Request(origin, {headers: {'Cf-Access-Jwt-Assertion': await token({email:'other@example.com'})}}), settings, keys));
  await assert.rejects(authenticatedEmail(new Request(origin, {headers: {'Cf-Access-Jwt-Assertion':good}}), {...settings, ACCESS_AUD:'different-app'}, keys));
  const expired = await new SignJWT({email}).setProtectedHeader({alg:'RS256',kid:'test-key'})
    .setIssuer('https://test-team.cloudflareaccess.com').setAudience('app-audience').setSubject('r')
    .setIssuedAt().setExpirationTime(Math.floor(Date.now()/1000)-60).sign(privateKey);
  await assert.rejects(authenticatedEmail(new Request(origin,{headers:{'Cf-Access-Jwt-Assertion':expired}}), settings, keys));
});

function env() {
  const calls: {kind: string; request: Request}[] = [];
  const result = {
    ...settings, PUBLIC_ORIGIN: origin,
    ASSETS: {fetch: async (request: Request) => {calls.push({kind:'asset',request});return new Response('<html>private app</html>');}},
    BACKEND: {fetch: async (request: Request) => {calls.push({kind:'backend',request});return Response.json({ok:true});}},
  };
  return {calls, value:result};
}

test('HTML, assets and API fail closed without configured or valid login', async () => {
  const {calls,value} = env();
  for (const path of ['/', '/assets/app.js', '/api/cases']) {
    assert.equal((await handle(new Request(origin+path), value)).status,401);
    assert.equal((await handle(new Request(origin+path), {...value,ACCESS_AUD:''})).status,503);
  }
  assert.equal(calls.length,0);
});

test('gateway replaces identity, strips supplied authorization and rejects CSRF and private files', async () => {
  const {calls,value} = env();
  const verified = async () => email;
  const response = await handle(new Request(origin+'/api/evaluate', {
    method:'POST',headers:{Origin:origin,'Content-Type':'application/json','x-c2a-user-email':'attacker@example.com',Authorization:'untrusted'},body:'{}',
  }), value, verified);
  assert.equal(response.status,200);
  assert.equal(response.headers.get('Cache-Control'),'no-store');
  assert.equal(calls[0].request.url,'https://crisis2action-api.internal/api/evaluate');
  assert.equal(calls[0].request.headers.get('x-c2a-user-email'),email);
  assert.equal(calls[0].request.headers.get('Host'),'crisis2action-api.internal');
  assert.equal(calls[0].request.headers.get('Authorization'),null);
  assert.equal((await handle(new Request(origin+'/api/evaluate',{method:'POST',headers:{Origin:'https://other.example'},body:'{}'}),value,verified)).status,403);
  assert.equal((await handle(new Request(origin+'/api/reviews',{method:'POST',body:'x'.repeat(65537)}),value,verified)).status,413);
  assert.equal((await handle(new Request(origin+'/Dataset/private.csv'),value,verified)).status,404);
  assert.equal((await handle(new Request('https://preview.example/api/cases'),value,verified)).status,403);
  assert.equal(calls.length,1);
});
