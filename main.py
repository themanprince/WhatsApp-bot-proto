import json
from fastapi import FastAPI, Body
import uvicorn
from dotenv import load_dotenv
from logger import logger


# Load the environment variables
load_dotenv()


app = FastAPI()

@app.post("/message")
def webhook(body = Body()):
	body_stringified = json.dumps(body)
	logger.info("Received request to webhook endpoint")
	logger.info(body_stringified)
	return {"content": body_stringified}
	
	

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8000))

	uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)