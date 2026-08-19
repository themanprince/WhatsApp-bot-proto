
* there is need for a _Verify Token_ ... this is a secret (created by you) known only to you and the API
* make sure fastapi's App reload option is set to False

* To send message to somebody, use the following request (expressed in curl format), replace phone number in "to" field with phone number of who you want to message, replace text value in "body" field with what you want to say

curl --request POST \
  --url https://graph.facebook.com/v25.0/<WHATSAPP_ID>/messages \
  --header 'Authorization: Bearer <YOUR_ACCESS_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "messaging_product": "whatsapp",
  "to": "2348037680836",
  "type": "text",
  "text": {
    "body": "Hello… this is a test message"
  }
}'

* the env var WHATSAPP_ID (as at the time of writing this), is that number in the url after graph.facebook.com/v25.0
