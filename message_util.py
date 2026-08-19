from dotenv import load_dotenv
import os
from fastapi import HTTPException
import requests



load_dotenv()


def send_message(to: str, body: str):
	whatsapp_id = os.environ.get("WHATSAPP_ID")
	access_token = os.environ.get("ACCESS_TOKEN")
	
	if (not whatsapp_id) or (not access_token):
		raise HTTPException(status_code=500, detail="missing required env var in function send_message")
	
	url = f"https://graph.facebook.com/v25.0/{whatsapp_id}/messages"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {access_token}"
	}
	body = {
		"messaging_product": "whatsapp",
		"to": to,
		"type": "text",
		"text": {
			"body": body
		}
	}
	
	response = requests.post(url, headers=headers, json=body)
	
	response.raise_for_status()
	
	return response.json()