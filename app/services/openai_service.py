from openai import AsyncOpenAI
from app.core.config import get_settings
import json

import os

settings = get_settings()

client = AsyncOpenAI(api_key=settings.openai_api_key)

def load_knowledge():
    knowledge_path = os.path.join(os.path.dirname(__file__), "..", "knowledge")
    content = ""
    for filename in ["faqs.txt", "sops.txt"]:
        file_path = os.path.join(knowledge_path, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content += f"\n--- {filename} ---\n"
                content += f.read()
    return content

SYSTEM_PROMPT_GENERAL_TEMPLATE = """
You are the General LMS Assistant for InfraCredit. 
Your role is to help users with:
1. Information about available courses.
2. Understanding Standard Operating Procedures (SOPs).
3. Answering Frequently Asked Questions (FAQs).
4. General platform navigation.

Note: Since the LMS API currently does not have explicit endpoints for SOPs/FAQs, 
the information below is retrieved from our internal Knowledge Base (KB) files.

Below is the internal knowledge base content:
{knowledge_base}

If you don't know the answer, advise the user to contact the HR or IT department.
Be professional, helpful, and concise.
"""

SYSTEM_PROMPT_COURSE = """
You are the Course-Only Assistant for InfraCredit. 
Your role is STRICTLY limited to answering questions about courses.
If a user asks about SOPs, FAQs (not related to courses), or other platform issues, 
politely inform them that you are only programmed to handle course-related queries 
and they should use the General Assistant for other matters.

Be professional and focus on course content, enrollment, and requirements.
"""

class OpenAIService:
    def __init__(self):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_courses",
                    "description": "Get a list of available courses from the LMS",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search": {"type": "string", "description": "Search term for courses"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_course_details",
                    "description": "Get detailed information about a specific course",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "course_id": {"type": "string", "description": "The unique ID of the course"}
                        },
                        "required": ["course_id"]
                    }
                }
            }
        ]

    async def chat(self, messages: list, bot_type: str = "general", lms_client=None):
        if bot_type == "general":
            knowledge = load_knowledge()
            system_prompt = SYSTEM_PROMPT_GENERAL_TEMPLATE.format(knowledge_base=knowledge)
        else:
            system_prompt = SYSTEM_PROMPT_COURSE
        
        # Prepend system prompt if not present
        if not messages or messages[0].get("role") != "system":
            messages.insert(0, {"role": "system", "content": system_prompt})
            
        # First call to OpenAI to check for tool usage
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=self.tools if lms_client else None,
            tool_choice="auto" if lms_client else None,
            temperature=0.7
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls and lms_client:
            # Add the assistant's message with tool calls to history
            messages.append(response_message)
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the appropriate LMS client method
                if function_name == "get_courses":
                    function_response = await lms_client.get_courses(search=function_args.get("search"))
                elif function_name == "get_course_details":
                    function_response = await lms_client.get_course_details(course_id=function_args.get("course_id"))
                else:
                    function_response = {"error": "Function not found"}

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                })
            
            # Second call to get the final answer after tool responses
            second_response = await client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
            )
            return second_response.choices[0].message.content

        return response_message.content

def get_openai_service():
    return OpenAIService()
