from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel, StopAtTools,function_tool,ModelSettings,RunContextWrapper
from agents.run import RunConfig
import os
from dotenv import load_dotenv


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


# def get_system_prompt(context:RunContextWrapper,agent:Agent):
#     print("[\ncontext]",context.context)
#     print("[\nagent]",agent)
#     return f"You are helpful assistant that can answer questions and help with tasks."


# @function_tool(is_enabled=False)
@function_tool
def get_weather(city : str) -> str:
    return f"the weather in {city} is sunny."
agent = Agent(
    name = "Weather and News Agent",
    instructions="You are a helpful Assistant",
    model = model,
    tools=[get_weather],
    model_settings=ModelSettings(
        tool_choice="none"
    )
)

result = Runner.run_sync(agent,"What is the Weather in karachi?")

print(result.final_output)
