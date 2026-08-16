import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

def send_prompt(prompt: str, verbose: bool) -> None:
    print("Hello from cli-ai-agent!")

    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise Exception("API key did not work")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages
    )
    if response.usage is None:
        raise("Something went wrong with the API call")
    
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    
    print(response.choices[0].message.content)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    send_prompt(args.user_prompt, args.verbose)
