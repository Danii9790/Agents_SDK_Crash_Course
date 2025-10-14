import asyncio
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv
from agents.run import AgentRunner,set_default_agent_runner
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

class CustomAgentRunner(AgentRunner):
    async def run(self,starting_agent,input,**Kwargs):
        print(f"CustomAgentRunner.run()")
        # Call parent with custom logic
        result = await super().run(starting_agent,input,**Kwargs)
        return result
set_default_agent_runner(CustomAgentRunner())
    

general_agent = Agent(name="General Agent")

async def main():

    result = await Runner.run(general_agent,"Hi")
    print(result.final_output)
    print("Last Agent : ",result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())