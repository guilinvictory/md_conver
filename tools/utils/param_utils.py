from typing import Any
from typing import Optional
from tools.utils.md_utils import MarkdownUtils
from tools.utils.mimetype_utils import MimeType


def get_md_string(tool_parameters: dict[str, Any], is_strip_wrapper: bool = False) -> str:
    answer = tool_parameters.get("answer")
    if not answer:
        raise ValueError("Empty input answer")

    if is_strip_wrapper:
        answer = MarkdownUtils.strip_markdown_wrapper(answer)

    return answer

def get_meta_data(mime_type: MimeType, output_filename: Optional[str]) -> dict[str, str]:
    if not MimeType:
        raise ValueError("Failed to generate meta data, mime_type is not defined")

    # normalize the filename
    result_filename: Optional[str] = None
    temp_filename = output_filename.strip() if output_filename else None
    if temp_filename:
        # ensure extension name
        extension = MimeType.get_extension(mime_type)
        if not temp_filename.lower().endswith(extension):
            temp_filename = f"{temp_filename}{extension}"
        result_filename = temp_filename

    return {
        "mime_type": mime_type,
        "url": result_filename,
    }