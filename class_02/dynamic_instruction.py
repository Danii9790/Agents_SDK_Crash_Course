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


def get_system_prompt(context,agent):
    print("[\ncontext]",context)
    print("[\nagent]",agent)
    return f"You are helpful assistant that can answer questions and help with tasks."

agent = Agent(
    name = "Weather and News Agent",
    instructions=get_system_prompt,
    model = model,
  

)

result = Runner.run_sync(agent,"Hi")

print(result.final_output)
