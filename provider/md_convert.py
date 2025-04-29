from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.md_to_docx.md_to_docx import MarkdownToDocxTool
from tools.md_to_pdf.md_to_pdf import MarkdownToPDFTool


class MdConvertProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            tool_arrays= [
                MarkdownToDocxTool,
                MarkdownToPDFTool
            ]
            for tool in tool_arrays:
                tool.from_credentials({})
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
