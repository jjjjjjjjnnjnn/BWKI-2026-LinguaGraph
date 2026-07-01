/**
 * LinguaGraph Survey Backend — Google Apps Script
 *
 * Deploy this as a Google Apps Script web app.
 * Data is written to the parent Google Sheet automatically.
 *
 * Deployment instructions:
 * 1. Create a new Google Sheet
 * 2. Extensions → Apps Script
 * 3. Paste this code
 * 4. Deploy → New deployment → Web app
 * 5. Set "Execute as: Me", "Who has access: Anyone"
 * 6. Copy the Web App URL
 * 7. Paste it into survey.html as ENDPOINT_URL
 */

function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Parse incoming JSON
    const data = JSON.parse(e.postData.contents);

    // Build header row if empty
    if (sheet.getLastRow() === 0) {
      const headers = [
        'Timestamp',
        'Response ID',
        'Language',
        'Duration (s)',
        'Topic Order',
        'Q1: ' + getTopic(data, 0),
        'Q2: ' + getTopic(data, 1),
        'Q3: ' + getTopic(data, 2),
        'Q4: ' + getTopic(data, 3),
        'Q5: ' + getTopic(data, 4),
        'Raw JSON'
      ];
      sheet.appendRow(headers);
    }

    // Extract responses
    const responses = data.responses || [];
    const row = [
      new Date().toISOString(),
      data.response_id || '',
      data.language || '',
      data.duration_seconds || '',
      (data.topic_order || []).map(t => t.topic_index).join(', '),
      (responses[0] || {}).text || '',
      (responses[1] || {}).text || '',
      (responses[2] || {}).text || '',
      (responses[3] || {}).text || '',
      (responses[4] || {}).text || '',
      JSON.stringify(data)
    ];

    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ success: true, id: data.response_id }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'running', endpoints: ['POST'] }))
    .setMimeType(ContentService.MimeType.JSON);
}

function getTopic(data, index) {
  try {
    const responses = data.responses || [];
    return responses[index]?.topic || 'Topic ' + (index + 1);
  } catch (e) {
    return 'Topic ' + (index + 1);
  }
}
