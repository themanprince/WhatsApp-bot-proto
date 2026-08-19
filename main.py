import json
from fastapi import FastAPI, Body, Query, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
from dotenv import load_dotenv
import os 
from typing import Any
from logger import logger
from message_util import send_message


# Load the environment variables
load_dotenv()


app = FastAPI()

#since meta requires a get endpoint which will be used to verify the webhook
@app.get("/", response_class=PlainTextResponse)
def verify(hub_mode:str = Query(alias="hub.mode"), hub_challenge:str = Query(alias="hub.challenge"), hub_verify_token:str = Query(alias="hub.verify_token")):
	my_verify_token = os.environ.get("VERIFY_TOKEN")
	if not my_verify_token:
		raise HTTPException(status_code=500, detail="please set necessary environment variables")
	
	if (hub_mode != "subscribe") or (hub_verify_token != my_verify_token):
		raise HTTPException(status_code=403, detail="verification failed")
	
	return PlainTextResponse(content=hub_challenge)
	

test_counter = 0	

@app.post("/")
def webhook(body: dict = Body(...)):
	global test_counter
	
	logger.info("Just received a POST to webhook URL")
	logger.info(json.dumps(body))
	
	if body["object"] == "whatsapp_business_account":
		for entry in body["entry"]:
			for change in entry["changes"]:
				value = change["value"]
				
				senderPhoneNumber: str | None = None
				if value:
					senderPhoneNumber = value["contacts"][0]["wa_id"]
				
				if not senderPhoneNumber:
					raise HTTPException(status_code=500, detail="failed to obtain phone number to reply to")
				
				if value["messages"]:
					for message in value["messages"]:
						body = f"this is response number {test_counter}"
						test_counter = test_counter + 1
						
						send_message(
							to = senderPhoneNumber,
							body = body
						)
						logger.info(f"sent message reply with content={body}")
	
	return PlainTextResponse("Event Received")
	
	

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8000))

	uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)