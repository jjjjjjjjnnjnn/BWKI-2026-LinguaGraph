/**
 * LinguaGraph Survey Relay — Cloudflare Worker
 *
 * Deploy this as a Cloudflare Worker.
 * It receives form POSTs from the survey frontend and relays them
 * to Google Apps Script, bypassing the GFW block.
 *
 * Deployment:
 * 1. Go to https://dash.cloudflare.com → Workers & Pages
 * 2. Create Worker → paste this code
 * 3. Deploy
 * 4. Copy the Worker URL (https://your-worker.workers.dev)
 * 5. Update survey.html ENDPOINT_URL to this Worker URL
 */

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // CORS headers for cross-origin requests from GitHub Pages
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  }

  // Handle CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders })
  }

  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 })
  }

  // Google Apps Script endpoint
  const GSHEET_URL = 'https://script.google.com/macros/s/AKfycbztARwvcBXrdXUE_SAPvAep1rFlsqcAtuZEx9mds2Vcjv4nUf1VtrrZyRyRqoNYE9iU/exec'

  try {
    // Get form data from the request
    const formData = await request.formData()
    const payload = formData.get('data')

    if (!payload) {
      return new Response(JSON.stringify({ success: false, error: 'No data field' }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 400,
      })
    }

    // Relay to Google Apps Script
    const relay = new URLSearchParams()
    relay.append('data', payload)

    const gsResponse = await fetch(GSHEET_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: relay.toString(),
    })

    const gsText = await gsResponse.text()

    return new Response(gsText, {
      headers: corsHeaders,
      status: 200,
    })

  } catch (err) {
    return new Response(JSON.stringify({ success: false, error: err.message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500,
    })
  }
}
