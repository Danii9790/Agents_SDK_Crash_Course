from gettext import find
from turtle import mode
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel, StopAtTools,function_tool,ModelSettings
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


@function_tool
def get_weather(city : str) -> str :
    return f"The weather in {city} is sunny"

@function_tool
def get_news(topic : str) -> str:
    return f"The news about {topic} is that it is good"

agent = Agent(
    name = "Weather and News Agent",
    instructions="Always reponsed in graceful and polite manner",
    model = model,
    tools=[get_weather,get_news],
    model_settings=ModelSettings(
        temperature=0.7,
        tool_choice="auto",
    ),
    # tool_use_behavior
    reset_tool_choice=False

)

result = Runner.run_sync(agent,"What is the weather in karachi and also share the news about karachi city.",max_turns=2)

print(result.final_output)
