# import asyncio
# from agents import Agent, AgentHooks, ModelSettings, RunConfig,Runner,AsyncOpenAI,OpenAIChatCompletionsModel
# import os 
# from dotenv import load_dotenv
# # import rich
# import asyncio

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# external_client = AsyncOpenAI(
#     api_key = os.environ['GEMINI_API_KEY'],
#     base_url=  "https://generativelanguage.googleapis.com/v1beta/openai"
# )

# model = OpenAIChatCompletionsModel(
#     model ="gemini-2.0-flash",
#     openai_client = external_client 
# )

# config = RunConfig(
#     model_provider= external_client,
#     model = model
# )
# settings = ModelSettings(
#     temperature=0.7,   # randomness (0 = deterministic, 1 = very random)
#     top_p=0.9,         # nucleus sampling (focus on top-p prob mass)
#     top_k=40,          # pick from top-k tokens
#     max_output_tokens=200,  # limit response length
   
# )
# class MyHooks(AgentHooks):
#     def before_run(self, ctx, agent, input):
#         print(f"[START] Agent {agent.name} with input: {input}")

#     def after_run(self, ctx, agent, result):
#         print(f"[END] Agent finished. Output: {result.final_output}")

#     def on_error(self, ctx, agent, error):
#         print(f"[ERROR] Agent {agent.name} failed: {error}")
# agent = Agent(
#     name = "Assistant",
#     instructions="You are a helpful Assistant",
#     model_settings=settings,
#     hooks= MyHooks()
# )
# async def main():
#     result = await Runner.run(agent,"write 50 words on Agentic AI." ,run_config= config)

#     print(result.final_output)

# asyncio.run(main())



# from agents import Agent, AgentHooks, ModelSettings, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# import os
# from dotenv import load_dotenv
# import rich

# load_dotenv()

# external_client = AsyncOpenAI(
#     api_key=os.environ['GEMINI_API_KEY'],
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model_provider=external_client,
#     model=model
# )

# settings = ModelSettings(
#     temperature=0.7,
#     top_p=0.9,
#     top_k=40,
#     max_output_tokens=150
# )

# class MyHooks(AgentHooks):
#     def before_run(self, ctx, agent, input):
#         print(f"\n[START] Agent '{agent.name}' is processing input: {input}")

#     def after_run(self, ctx, agent, result):
#         print(f"[END] Agent '{agent.name}' finished. Output: {result.final_output}")

#     def on_error(self, ctx, agent, error):
#         print(f"[ERROR] Agent '{agent.name}' failed: {error}")

# agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful Assistant.",
#     model_settings=settings,
#     hooks=MyHooks()
# )

# prompts = [
#     "Write 30 words on Agentic AI.",
#     "Explain the concept of autonomy in AI in 20 words.",
#     "Give an example of Agentic AI in real life."
# ]

# import asyncio

# async def main():
#     for i, prompt in enumerate(prompts, start=1):
#         print(f"\n--- TURN {i} ---")
#         result = await Runner.run(agent, prompt, run_config=config)
#         rich.print(f"FINAL OUTPUT [{i}]: {result.final_output}")

# if __name__ == "__main__":
#     asyncio.run(main())


# from agents import Agent, AgentHooks, ModelSettings, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # -----------------------------
# # Gemini Client
# # -----------------------------
# external_client = AsyncOpenAI(
#     api_key=os.environ['GEMINI_API_KEY'],
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model_provider=external_client,
#     model=model
# )

# # -----------------------------
# # Model Settings
# # -----------------------------
# settings = ModelSettings(
#     temperature=0.7,
#     top_p=0.9,
#     top_k=40,
#     max_output_tokens=150
# )

# # -----------------------------
# # Hooks
# # -----------------------------
# class MyHooks(AgentHooks):
#     def before_run(self, ctx, agent, input):
#         print(f"[HOOK] START - Agent '{agent.name}' received input: {input}")

#     def after_run(self, ctx, agent, result):
#         print(f"[HOOK] END   - Agent '{agent.name}' output: {result.final_output}")

#     def on_error(self, ctx, agent, error):
#         print(f"[HOOK] ERROR - Agent '{agent.name}' failed: {error}")

# # -----------------------------
# # Agent
# # -----------------------------
# agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful AI assistant.",
#     model_settings=settings,
#     hooks=MyHooks()
# )

# # -----------------------------
# # Prompts
# # -----------------------------
# prompts = [
#     "Write 30 words on Agentic AI.",
#     "Explain autonomy in AI in 20 words.",
#     "Give an example of Agentic AI in real life."
# ]

# # -----------------------------
# # Run using run_sync
# # -----------------------------
# for i, prompt in enumerate(prompts, start=1):
#     print(f"\n--- TURN {i} ---")
#     # run_sync triggers hooks automatically
#     result = Runner.run_sync(agent, prompt, run_config=config)
#     print(f"FINAL OUTPUT [{i}]: {result.final_output}")


from agents import Agent, AgentHooks, ModelSettings, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# LLM client
# -----------------------------
external_client = AsyncOpenAI(
    api_key=os.environ['GEMINI_API_KEY'],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model_provider=external_client,
    model=model
)

# -----------------------------
# Agent hooks
# -----------------------------
class ChatHooks(AgentHooks):
    def before_run(self, ctx, agent, input_text):
        print(f"[HOOK] START - Agent '{agent.name}' received input: {input_text}")

    def after_run(self, ctx, agent, result):
        print(f"[HOOK] END   - Agent '{agent.name}' output: {result.final_output}")

    def on_error(self, ctx, agent, error):
        print(f"[HOOK] ERROR - Agent '{agent.name}' failed: {error}")

# -----------------------------
# Agent settings
# -----------------------------
settings = ModelSettings(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    max_output_tokens=150
)

agent = Agent(
    name="SupportBot",
    instructions="You are a helpful customer support assistant.",
    model_settings=settings,
    hooks=ChatHooks()
)

# -----------------------------
# Simulate chat with hooks manually
# -----------------------------
prompts = [
    "Hi, I want to return my order.",
    "The order number is 12345.",
    "Can I get a refund or exchange?"
]

for i, prompt in enumerate(prompts, start=1):
    print(f"\n--- USER TURN {i} ---")
    ctx = {}  # context for hooks

    # Manually trigger hooks before LLM call
    agent.hooks.before_run(ctx, agent, prompt)

    try:
        # Call LLM
        result = Runner.run_sync(agent, prompt, run_config=config)

        # Manually trigger hooks after LLM call
        agent.hooks.after_run(ctx, agent, result)

        print(f"FINAL OUTPUT [{i}]: {result.final_output}")

    except Exception as e:
        # Trigger error hook
        agent.hooks.on_error(ctx, agent, e)
