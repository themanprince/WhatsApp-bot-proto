import json
from fastapi import FastAPI, Body, Query, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
from dotenv import load_dotenv
import os 
from typing import Any
from logger import logger


# Load the environment variables
load_dotenv()


app = FastAPI()

#since meta requires a get endpoint which will be used to verify the webhook
@app.get("/")
def verify(hub_mode:str = Query(alias="hub.mode"), hub_challenge:str = Query(alias="hub.challenge"), hub_verify_token:str = Query(alias="hub.verify_token")) -> str:
	my_verify_token = os.environ.get("VERIFY_TOKEN")
	if not my_verify_token:
		raise HTTPException(status=500, detail="please set necessary environment variables")
	
	if (hub_mode != "subscribe") or (hub_verify_token != my_verify_token):
		raise HTTPException(status=403, detail="verification failed")
	
	return PlainTextResponse(content=hub_challenge)
	
	

@app.post("/")
def webhook(body: dict[str, Any] = Body(...)):
	body_stringified = json.dumps(body)
	logger.info("Received request to webhook endpoint")
	logger.info(body_stringified)
	return {"content": body_stringified}
	
	

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8000))

	uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)