# Orchestration Using Code.

from __future__ import annotations
import asyncio
from dataclasses import dataclass
from typing import List, Literal
from agents import Agent,ItemHelpers,Runner,TResponseInputItem,trace,AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )

model = OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=provider
    )

config = RunConfig(
        model=model,
        model_provider=provider
    )

story_outline_generator = Agent(
    name="Story outline_generator",
    instructions="You generate a very short outline based on the user's input."
    "If there is any feedback provided , use it to improve the Outline."
)

@dataclass
class EvaluationFeedback:
    feedback : str
    score : Literal["pass","needs_improvement","fail"]

evaluator = Agent[None](
    name  = "Evalutor",
    instructions=(
        "You evaluate a story outline and decide if it's good enough. "
        "If it's not good enough, you provide feedback on what needs to be improved. "
        "Never give it a pass on the first try. After 5 attempts, you can give it a pass if the story outline is good enough - do not go for perfection"
    ),
    output_type=EvaluationFeedback
)

async def main():
    msg = input("What Kind of story would you like to hear? : ")
    input_items : List[TResponseInputItem] = [{"content":msg,"role": "user"}]
    latest_outline : str | None = None

    with trace("LLM as a jugde"):
        while True:
            story_outline_result = await Runner.run(
                story_outline_generator,input_items
            )
        
            input_items = story_outline_result.to_input_list()
            # latest_outline = ItemHelpers.text_message_output(story_outline_result.new_items)
            latest_outline = ItemHelpers.text_message_output(story_outline_result.new_items[0])

            print("Story outline Generator")

            evaluator_result = await Runner.run(evaluator,input_items)
            result : EvaluationFeedback = evaluator_result.final_output
            print(f"Evaulator score : {result.score}")

            if result.score == "pass":
                print("Story outline is good enough,excitied..")
                break

            print("Re-running with feedback")

            input_items.append({"content":f"Feedback : {result.feedback}","role":"user"})
        print(f"Final story outline : {latest_outline}")


if __name__ == "__main__":
    asyncio.run(main())