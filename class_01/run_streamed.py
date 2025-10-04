import asyncio
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel, function_tool
import os
from agents.model_settings import ModelSettings
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
    # tracing_disabled= True,
    # workflow_name="Run_Streamed",
    # model_settings=ModelSettings(
    #     temperature=0.7,
    #     top_p=0.9,
    #     top_k=40,
    #     max_output_tokens=150
    # )
)



# ❌ remove @function_tool here
async def get_weather(city: str) -> str:
    print("\nBefore Sleep\n")
    await asyncio.sleep(5)
    print("\nAwake Up\n")
    return f"The weather in {city} is sunny."


# ✅ decorate only the safe wrapper
@function_tool
async def safe_get_weather(city: str) -> str:
    try:
        return await asyncio.wait_for(get_weather(city), timeout=3)
    except asyncio.TimeoutError:
        return "⚠️ Sorry, the weather service is taking too long. Please try again later."
    except Exception as e:
        return f"❌ Oops! Something went wrong: {str(e)}"

agent = Agent(
    name="Agent",
    tools=[safe_get_weather]  # use safe wrapper
)

async def main():
    result = Runner.run_streamed(agent, "What is the Weather in Karachi",run_config=config)

    async for event in result.stream_events():
        rich.print(f"[Event] : {event}")

if __name__ == "__main__":
    asyncio.run(main())



# @function_tool
# async def get_weather(city:str) ->str:
#     print("\nBefore Sleep\n")
#     await asyncio.sleep(5)
#     print("\nAwake Up\n")
#     return f"The weather in {city} is sunny."


# agent = Agent(
#     name= "Agent",
#     tools=[get_weather]
# )

# async def main():
#     result = Runner.run_streamed(agent,"What is the Weather in karachi",run_config=config)

#     async for event in result.stream_events():
#        rich.print(f"[Event] : {event}" )

# if __name__ == "__main__":
#     asyncio.run(main())

