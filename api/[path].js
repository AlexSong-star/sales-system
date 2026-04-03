const RAILWAY = 'https://sales-system-production-0a91.up.railway.app'

export default async function handler(req) {
  const path = req.query.path || ''
  const url = `${RAILWAY}/${path}${req.url.includes('?') ? '?' + req.url.split('?')[1] : ''}`

  try {
    const response = await fetch(url, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
        ...(req.headers || {})
      },
      body: ['POST', 'PATCH', 'PUT'].includes(req.method) ? await req.text() : undefined
    })

    const data = await response.text()
    return new Response(data, {
      status: response.status,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': '*',
        'Content-Type': response.headers.get('content-type') || 'application/json'
      }
    })
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Proxy error', detail: err.message }), {
      status: 502,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    })
  }
}

export const config = {
  api: {
    bodyParser: false,
  },
}
