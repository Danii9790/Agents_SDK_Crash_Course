# fastfood_bot.py
import os
import json
import requests
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.tool import function_tool
from agents.run import RunConfig

# Load env variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")  # Meta access token
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")  # Phone Number ID

# FastAPI app
app = FastAPI()

# ---------------------------
# Agent Initialization
# ---------------------------
async def create_agent():
    provider = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=provider
    )

    config = RunConfig(
        model=model,
        model_provider=provider
    )

    @function_tool("get_menu")
    def get_menu() -> str:
        # Return your fast food menu
        return json.dumps({
            "menu": [
                {"name": "Burger", "price": 200},
                {"name": "Pizza", "price": 500},
                {"name": "Cold Drink", "price": 100}
            ]
        })

    agent = Agent(
        name="FastFoodBot",
        instructions="""
        You are a fast food WhatsApp assistant. 
        Show menu, take orders, calculate total, get location and confirm orders.
        Use `get_menu` tool to fetch menu items when user asks for it.
        """,
        model=model,
        tools=[get_menu]
    )

    return agent, config

# ---------------------------
# Helper function to send WhatsApp messages
# ---------------------------
def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    # WhatsApp number should not contain '+'
    if to.startswith('+'):
        to = to.replace('+', '')

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(url, headers=headers, json=data)
    print("🔹 WhatsApp API response:", response.status_code, response.text)
    return response.json()

# ---------------------------
# Webhook endpoint
# ---------------------------
@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    try:
        messages = payload['entry'][0]['changes'][0]['value'].get('messages', [])
        if not messages:
            return JSONResponse(content={"status": "no messages"})

        sender = messages[0]['from']
        text = messages[0]['text']['body']

        # Run Agent SDK
        agent, config = await create_agent()
        agent_response = await Runner.run(agent, input=text, run_config=config)  # <-- fix here
        reply_text = getattr(agent_response, "final_output", None) or str(agent_response)

        # Send response back to user
        send_whatsapp_message(sender, reply_text)

        return JSONResponse(content={"status": "ok"})

    except Exception as e:
        return JSONResponse(content={"status": "error", "error": str(e)})

# ---------------------------
# Optional: Verification endpoint (GET) for WhatsApp
# ---------------------------
@app.get("/webhook")
async def verify_webhook(request: Request):
    verify_token = os.getenv("VERIFY_TOKEN", "fastfood_verify")
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode and token:
        if mode == "subscribe" and token == verify_token:
            return JSONResponse(content=int(challenge))
    return JSONResponse(content="Invalid verification token")
