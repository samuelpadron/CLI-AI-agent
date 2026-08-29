from typing import cast
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from openai.types.chat import ChatCompletionToolUnionParam


available_functions: list[ChatCompletionToolUnionParam] = [
    cast(ChatCompletionToolUnionParam, schema_get_files_info),
    cast(ChatCompletionToolUnionParam, schema_get_file_content),
    cast(ChatCompletionToolUnionParam, schema_write_file),
    cast(ChatCompletionToolUnionParam, schema_run_python_file),
]