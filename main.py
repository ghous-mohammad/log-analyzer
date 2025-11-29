import itertools
import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner
from agents import Agent, Runner, function_tool, ModelSettings, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled

load_dotenv()
set_tracing_disabled(disabled=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # 🔑 Get your API key from environment
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"  # 🌐 Gemini-compatible base URL (set this in .env file)

# 🌐 Initialize the AsyncOpenAI-compatible client with Gemini details
external_client: AsyncOpenAI = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

log_file_path = "./logs/Linux_2k.log"
prompt_url = "./prompts/prompt.txt"
start_line = 1
end_line = 50

prompt=""

@function_tool
def logs_func():
    lines_out = []
    try:
        with open(log_file_path, "r") as file:
            lines = itertools.islice(file, start_line, end_line)

            for line in lines:
            
                lines_out.append(line.rstrip("\n"))
   
    except FileNotFoundError:
        return f"Please check your file path '{log_file_path}' was not found"
    except Exception as e:
        return f"An error occurred: {e}"
    return {"logs": lines_out}






# re = logs_func()
# print(re)
try:
    with open(prompt_url, "r") as text:
        for line in text:
            prompt += line

except FileNotFoundError:
    print(f"Please check your file path '{log_file_path}' was not found")

except Exception as e:
    print(f"An error occured: {e}")

log_analyzer_agent = Agent(
    name="log_analyzer",
    instructions=prompt,
    model= model,
    tools= [logs_func]
    )


async def runner():
    result = await Runner().run(log_analyzer_agent, "summary of analyzed logs")
    return result.final_output

value = asyncio.run(runner())
print(value)
