import os
from dotenv import load_dotenv

from task.client import DialClient
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role
from task.prompts import SYSTEM_PROMPT
from task.tools.users.create_user_tool import CreateUserTool
from task.tools.users.delete_user_tool import DeleteUserTool
from task.tools.users.get_user_by_id_tool import GetUserByIdTool
from task.tools.users.search_users_tool import SearchUsersTool
from task.tools.users.update_user_tool import UpdateUserTool
from task.tools.users.user_client import UserClient
from task.tools.web_search import WebSearchTool

load_dotenv()
DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com"
API_KEY = os.getenv('DIAL_API_KEY')

def main():
    print(API_KEY)
    #TODO:
    # 1. Create UserClient
    user_client = UserClient()
    # 2. Create DialClient with all tools (WebSearchTool, GetUserByIdTool, SearchUsersTool, CreateUserTool, UpdateUserTool, DeleteUserTool)
    dial_client = DialClient(
        endpoint=DIAL_ENDPOINT,
        deployment_name="gpt-4o",
        api_key=API_KEY,
        tools=[
            WebSearchTool(api_key=API_KEY, endpoint=DIAL_ENDPOINT),
            GetUserByIdTool(user_client),
            SearchUsersTool(user_client),
            CreateUserTool(user_client),
            UpdateUserTool(user_client),
            DeleteUserTool(user_client),
        ]
    )
    # 3. Create Conversation and add there first System message with SYSTEM_PROMPT (you need to write it in task.prompts#SYSTEM_PROMPT)
    conversation = Conversation()
    conversation.add_message(Message(role=Role.SYSTEM, content=SYSTEM_PROMPT))
    # 4. Run infinite loop and in loop and:
    print("Type your question or 'exit' to quit.")
    while True:
    #    - get user input from terminal (`input("> ").strip()`)
        user_input = input("> ").strip()
    #    - Add User message to Conversation
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break
        conversation.add_message(Message(role=Role.USER, content=user_input))
    #    - Call DialClient with conversation history
        ai_message = dial_client.get_completion(conversation.get_messages(), print_request=True)
    #    - Add Assistant message to Conversation and print its content
        conversation.add_message(ai_message)
        print("AI:", ai_message.content)
        print("---" * 40)


main()

#TODO:
# Request sample:
# Add Andrej Karpathy as a new user