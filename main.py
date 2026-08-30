import os
import sys
import json
import argparse
from dotenv import load_dotenv
from typing import cast
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from prompts import system_prompt
from call_function import available_functions, call_function

def initiate_agent(prompt: str) -> tuple[OpenAI, list[ChatCompletionMessageParam]]:
    print("Hello from cli-ai-agent!")

    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise Exception("API key did not work")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    initial_messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    
    return client, initial_messages

def converse(client: OpenAI, messages: list[ChatCompletionMessageParam],verbose: bool):
        

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages= messages,
            tools=available_functions
        )
        
        if response.usage is None:
            raise Exception("Something went wrong with the API call")
        
        if verbose:
            print(f"System prompt: {system_prompt}")
            print(f"User prompt: {prompts[-1]}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        
        message = response.choices[0].message
        
        messages.append(cast(ChatCompletionMessageParam,message))
        
        if message.tool_calls:
            for call in message.tool_calls:
                if call.type == "function":
                    function_args = json.loads(call.function.arguments or "{}")
                    print(f"Calling function: {call.function.name}({function_args})")
                    result_message = call_function(call, verbose)
                    
                    if not result_message["content"]:
                        raise Exception("Error: tool message has no content")
                    
                    if verbose:
                        print(f"-> {result_message['content']}")
                        
                    messages.append(cast(ChatCompletionMessageParam,result_message))
                        
        else:
            print(message.content)
            return
        
    return -1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    client, prompts = initiate_agent(args.user_prompt)
    converse(client, prompts, args.verbose)
