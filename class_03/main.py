import asyncio
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel, function_tool,handoff
from agents.extensions import handoff_filters
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
@function_tool
def get_weather(city : str) -> str:
    return f"The weather in {city} is sunny."

refund_agent = Agent(name="Refund Agent")
general_agent = Agent(name="General Agent",
tools=[get_weather],
handoffs=[handoff(agent=refund_agent,tool_name_override="Refund_order",tool_description_override="Refund the order"
,is_enabled=True
,input_filter=handoff_filters.remove_all_tools

)])

async def main():
    result = await Runner.run(general_agent,"""
    What is the weather in karachi and also
    I want to refund my order . order nummber is (546890) amount = 2000
    """)
    print(result.final_output)
    print("Last Agent : ",result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())