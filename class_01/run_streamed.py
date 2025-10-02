import asyncio
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel, function_tool
import os
# from agents.model_settings import ModelSettings
from dotenv import load_dotenv
from agents import RunConfig
from agents import enable_verbose_stdout_logging
import rich

enable_verbose_stdout_logging()

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Api key is not Set..")

external_provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= external_provider
)

config = RunConfig(
    model_provider= external_provider,
    model = model,
    tracing_disabled= True,
    # workflow_name="Run_Streamed",
    # model_settings=ModelSettings(
    #     temperature=0.7,
    #     top_p=0.9,
    #     top_k=40,
    #     max_output_tokens=150
    # )
)

@function_tool
def get_weather(city:str) ->str:
    return f"The weather in {city} is sunny."


agent = Agent(
    name= "Agent",
    tools=[get_weather]
)

async def main():
    result = Runner.run_streamed(agent,"What is the Weather in karachi",run_config=config)

    async for event in result.stream_events():
       rich.print(f"[Event] : {event}" )

if __name__ == "__main__":
    asyncio.run(main())
