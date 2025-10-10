import asyncio
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel, function_tool,handoff,RunContextWrapper
from agents.extensions import handoff_filters
import os
from dotenv import load_dotenv
from agents.agent import StopAtTools
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key= api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash-exp",
    openai_client= external_client
)

class CurrentUser(BaseModel):
    is_logged_in : bool

# Callable[[RunContextWrapper[Any],Agent[Any]],MaybeAwaitable[bool]]
def can_customer_refund(local_context : RunContextWrapper[CurrentUser],agent:Agent[CurrentUser]) -> bool:
    print("Local context : ",local_context.context)
    if local_context.context and local_context.context.is_logged_in:
        return True
    return False
    
refund_agent = Agent(name="Refund Agent")
general_agent = Agent(name="General Agent",
handoffs=[handoff(agent=refund_agent,is_enabled=can_customer_refund,
)])

async def main():
    current_user = CurrentUser(is_logged_in=True)
    result = await Runner.run(general_agent,"""
    I want to refund my order .
    Detail Order : nummber is (546890)
    Amount = 2000
    """,context=current_user)
    print(result.final_output)
    print("Last Agent : ",result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())