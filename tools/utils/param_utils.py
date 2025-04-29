from typing import Any

from tools.utils.md_utils import MarkdownUtils


def get_md_string(tool_parameters: dict[str, Any], is_strip_wrapper: bool = False) -> str:
    answer = tool_parameters.get("answer")
    if not answer:
        raise ValueError("Empty input answer")

    if is_strip_wrapper:
        answer = MarkdownUtils.strip_markdown_wrapper(answer)

    return answer
