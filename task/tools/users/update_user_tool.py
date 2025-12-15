from typing import Any

from task.tools.users.base import BaseUserServiceTool
from task.tools.users.models.user_info import UserUpdate


class UpdateUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        #Provide tool name as `update_user`
        return "update_user"

    @property
    def description(self) -> str:
        #Provide description of this tool
        return 'Updates user'

    @property
    def input_schema(self) -> dict[str, Any]:
        # Provide tool params Schema:
        # - id: number, required, User ID that should be updated.
        # - new_info: UserUpdate.model_json_schema()
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "User ID that should be updated."
                },
                "new_info": UserUpdate.model_json_schema()
            },
            "required": ["id"]
        }

    def execute(self, arguments: dict[str, Any]) -> str:
        try:
            # 1. Get user `id` from `arguments`
            user_id = arguments["id"]
            # 2. Get `new_info` from `arguments` and create `UserUpdate` via pydentic `UserUpdate.model_validate`
            user = UserUpdate.model_validate(arguments["new_info"])
            # 3. Call user_client update_user and return its results
            return self._user_client.update_user(user_id=user_id, user_update_model=user)
        # 4. Optional: You can wrap it with `try-except` and return error as string `f"Error while creating a new user: {str(e)}"`
        except Exception as e:
            return f"Error while creating a new user: {str(e)}"
