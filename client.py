import asyncio
import json
import os
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
import yaml
from mistralai import Mistral

MODEL_NAME = "mistral-large-latest"
load_dotenv()

mcp_client = Client(StreamableHttpTransport("http://127.0.0.1:8010/mcp"))
mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


async def get_mcp_tools():
    """Get available MCP tools and convert them to Mistral function format"""
    async with mcp_client:
        tools = await mcp_client.list_tools()
        
        # Convert MCP tools to Mistral function format
        mistral_functions = []
        for tool in tools:
            mistral_functions.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": tool.inputSchema.get("properties", {}),
                        "required": tool.inputSchema.get("required", [])
                    }
                }
            })
        
        return mistral_functions

async def execute_mcp_tool(tool_name: str, arguments: dict):
    """Execute an MCP tool with given arguments"""
    async with mcp_client:
        try:
            result = await mcp_client.call_tool(tool_name, arguments)
            return result
        except Exception as e:
            return f"Error executing tool {tool_name}: {e}"

async def chat_with_tools(user_message: str):
    """Chat with Mistral using MCP tools"""
    # Get available tools
    tools = await get_mcp_tools()
    
    messages = yaml.safe_load(open('prompts/agent-system-prompt.yaml', 'r'))["messages"]
    messages.append({
            "role": "user",
            "content": user_message
        })
    
    # Call Mistral with function calling
    response = mistral_client.chat.complete(
        model=MODEL_NAME,
        messages=messages,
        tools=tools
    )
    
    # Check if Mistral wants to call a tool
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            # Execute the MCP tool
            tool_result = await execute_mcp_tool(tool_name, tool_args)
            
            # Add the assistant's response with tool calls to the conversation
            messages.append({
                "role": "assistant",
                "content": response.choices[0].message.content or "",
                "tool_calls": response.choices[0].message.tool_calls
            })
            
            # Add the tool result to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result)
            })
            
            # Get final response from Mistral
            final_response = mistral_client.chat.complete(
                model=MODEL_NAME,
                messages=messages,
                tools=tools
            )
            
            return final_response.choices[0].message.content
    
    return response.choices[0].message.content

async def main():
    """Interactive chat loop with MCP tools"""
    print("=" * 60)
    print("Welcome to the Interactive MCP Chat!")
    print("=" * 60)
    print("Type your questions and press Enter.")
    print("Type 'exit', 'quit', or 'q' to end the session.")
    print("=" * 60)
    print()
    
    while True:
        try:
            # Get user input
            user_query = input("You: ").strip()
            
            # Check for exit commands
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            # Skip empty queries
            if not user_query:
                continue
            
            # Get response from chat_with_tools
            print("\nAssistant: ", end="", flush=True)
            response = await chat_with_tools(user_query)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print()


if __name__ == "__main__":
    asyncio.run(main())