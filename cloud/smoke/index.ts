// LOCAL TEST HARNESS ONLY. Never deploy this unauthenticated test proxy.
// It tests the private deployed Python Worker through Wrangler's authenticated
// remote binding. There is no test bypass in the production gateway.
export default {
  async fetch(request: Request, env: {BACKEND: Fetcher; ASSETS: Fetcher}) {
    const url = new URL(request.url);
    if (!['127.0.0.1', 'localhost'].includes(url.hostname)) return new Response('Local tests only', {status:403});
    if (url.pathname.startsWith('/api/')) {
      const headers = new Headers({'x-c2a-user-email':'francescogabrielg@gmail.com'});
      headers.set('Host','crisis2action-api.internal');
      if (request.headers.has('Content-Type')) headers.set('Content-Type',request.headers.get('Content-Type')!);
      headers.set('Origin','https://crisis2action.spunto-speak.workers.dev');
      let body: ReadableStream | string | null = request.body;
      if (url.pathname === '/api/reviews' && request.method === 'POST') {
        const review = await request.json<{note:string}>();
        review.note = `[AUTOMATED CLOUD TEST] ${review.note}`;
        body = JSON.stringify(review);
      }
      return env.BACKEND.fetch(new Request(`https://crisis2action-api.internal${url.pathname}${url.search}`, {
        method:request.method, headers, body,
      }));
    }
    if (url.pathname === '/' || url.pathname === '/index.html' || /^\/assets\/[a-zA-Z0-9_./-]+\.(js|css|svg|png|ico|woff2?)$/.test(url.pathname)) {
      return env.ASSETS.fetch(request);
    }
    return new Response('Not found',{status:404});
  }
};
