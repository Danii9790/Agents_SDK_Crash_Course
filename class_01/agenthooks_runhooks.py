from agents import Agent, AgentHooks, ModelSettings, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# LLM Client Setup
# -----------------------------
external_client = AsyncOpenAI(
    api_key=os.environ['GEMINI_API_KEY'],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(model_provider=external_client, model=model)

settings = ModelSettings(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    max_output_tokens=150
)

# -----------------------------
# Permanent AgentHooks
# -----------------------------
class MyAgentHooks(AgentHooks):
    def before_run(self, ctx, agent, input):
        print(f"[AGENTHOOK] START - Agent '{agent.name}' input: {input}")

    def after_run(self, ctx, agent, result):
        print(f"[AGENTHOOK] END   - Agent '{agent.name}' output: {result.final_output}")

    def on_error(self, ctx, agent, error):
        print(f"[AGENTHOOK] ERROR - Agent '{agent.name}' failed: {error}")

# -----------------------------
# Temporary RunHooks (for a specific run)
# -----------------------------
class MyTempHooks(AgentHooks):
    def before_run(self, ctx, agent, input):
        print(f"[TEMPHOOK] START - Temporary hook input: {input}")

    def after_run(self, ctx, agent, result):
        print(f"[TEMPHOOK] END   - Temporary hook output: {result.final_output}")

# -----------------------------
# Create Agent
# -----------------------------
agent = Agent(
    name="DemoLLMAgent",
    instructions="You are a helpful Assistant.",
    model_settings=settings,
    hooks=MyAgentHooks()  # permanent hooks
)

# -----------------------------
# Prompts
# -----------------------------
prompts = [
    "Explain Agentic AI in simple words.",
    "Give a real-world example of autonomous AI.",
    "Why are AI hooks useful for debugging?"
]

for i, prompt in enumerate(prompts, start=1):
    print(f"\n--- TURN {i} ---")
    
    # Use temporary hooks only on turn 2
    if i == 2:
        original_hooks = agent.hooks
        agent.hooks = MyTempHooks()  # temporary hooks
        result = Runner.run_sync(agent, prompt, run_config=config)
        agent.hooks = original_hooks  # restore permanent hooks
    else:
        result = Runner.run_sync(agent, prompt, run_config=config)
    
    print(f"FINAL OUTPUT [{i}]: {result.final_output}")
from agents import Agent, AgentHooks, ModelSettings, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# LLM Client Setup
# -----------------------------
external_client = AsyncOpenAI(
    api_key=os.environ['GEMINI_API_KEY'],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(model_provider=external_client, model=model)

settings = ModelSettings(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    max_output_tokens=150
)

# -----------------------------
# Permanent AgentHooks
# -----------------------------
class MyAgentHooks(AgentHooks):
    def before_run(self, ctx, agent, input):
        print(f"[AGENTHOOK] START - Agent '{agent.name}' input: {input}")

    def after_run(self, ctx, agent, result):
        print(f"[AGENTHOOK] END   - Agent '{agent.name}' output: {result.final_output}")

    def on_error(self, ctx, agent, error):
        print(f"[AGENTHOOK] ERROR - Agent '{agent.name}' failed: {error}")

# -----------------------------
# Temporary RunHooks (for a specific run)
# -----------------------------
class MyTempHooks(AgentHooks):
    def before_run(self, ctx, agent, input):
        print(f"[TEMPHOOK] START - Temporary hook input: {input}")

    def after_run(self, ctx, agent, result):
        print(f"[TEMPHOOK] END   - Temporary hook output: {result.final_output}")

# -----------------------------
# Create Agent
# -----------------------------
agent = Agent(
    name="DemoLLMAgent",
    instructions="You are a helpful Assistant.",
    model_settings=settings,
    hooks=MyAgentHooks()  # permanent hooks
)

# -----------------------------
# Prompts
# -----------------------------
prompts = [
    "Explain Agentic AI in simple words.",
    "Give a real-world example of autonomous AI.",
    "Why are AI hooks useful for debugging?"
]

for i, prompt in enumerate(prompts, start=1):
    print(f"\n--- TURN {i} ---")
    
    # Use temporary hooks only on turn 2
    if i == 2:
        original_hooks = agent.hooks
        agent.hooks = MyTempHooks()  # temporary hooks
        result = Runner.run_sync(agent, prompt, run_config=config)
        agent.hooks = original_hooks  # restore permanent hooks
    else:
        result = Runner.run_sync(agent, prompt, run_config=config)
    
    print(f"FINAL OUTPUT [{i}]: {result.final_output}")
