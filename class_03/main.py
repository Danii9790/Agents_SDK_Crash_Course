import asyncio
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,handoff
from agents.run import RunConfig
import os
from dotenv import load_dotenv
from agents.agent import StopAtTools


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

refund_agent = Agent(name="Refund Agent")
general_agent = Agent(name="General Agent",handoffs=[handoff(agent=refund_agent,tool_name_override="Refund order",tool_description_override="Refund the order")])

async def main():
    result = await Runner.run(general_agent,"I want to refund my order.")
    print(result.final_output)
    print("Last Agent : ",result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())