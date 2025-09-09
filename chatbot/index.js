// index.js
const dialogflow = require('dialogflow');
const uuid = require('uuid');

// A unique identifier for the session
const sessionId = uuid.v4();

async function runSample() {
  // Create a new session
  const sessionClient = new dialogflow.SessionsClient({
    keyFilename: 'chatbot-key.json'
  });
  const sessionPath = sessionClient.sessionPath('chatbot-project-471618', sessionId);

  // The text query
  const request = {
    session: sessionPath,
    queryInput: {
      text: {
        text: 'Hello',  // test message
        languageCode: 'en-US',
      },
    },
  };

  // Send request and log result
  const responses = await sessionClient.detectIntent(request);
  console.log('Detected intent');
  const result = responses[0].queryResult;
  console.log(`  Query: ${result.queryText}`);
  console.log(`  Response: ${result.fulfillmentText}`);
}

runSample();
