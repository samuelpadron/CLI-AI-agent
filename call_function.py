from typing import cast
from functions.get_files_info import schema_get_files_info
from openai.types.chat import ChatCompletionToolUnionParam

available_functions: list[ChatCompletionToolUnionParam] = [
    cast(ChatCompletionToolUnionParam, schema_get_files_info),
]