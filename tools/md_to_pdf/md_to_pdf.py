import logging
from typing import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from xhtml2pdf import pisa

from tools.utils.md_utils import MarkdownUtils
from tools.utils.mimetype_utils import MimeType
from tools.utils.param_utils import get_md_string


class MarkdownToPDFTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:

        answer = get_md_string(tool_parameters, is_strip_wrapper=True)
        print(answer)
        try:
            html_str = self._convert_to_html(answer)
            result_file_bytes = pisa.CreatePDF(
                src=html_str,
                dest_bytes=True,
                encoding="utf-8",
            )
        except Exception as e:
            logging.exception("转换失败")
            yield self.create_text_message(f"生成pdf失败, error: {str(e)}")
            return

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta={"mime_type": MimeType.PDF},
        )

    @staticmethod
    def _convert_to_html(answer: str) -> str:
        html_str = MarkdownUtils.convert_markdown_to_html(answer)
        # 字体配置
        font_families = ",".join(
            [
                "Sans-serif",  # for English
                "STSong-Light",  # for Simplified Chinese
                "MSung-Light",  # for Traditional Chinese
                "HeiseiMin-W3",  # for Japanese
            ]
        )
        css_style = f"""
        <style>
            html {{
                -pdf-word-wrap: CJK;
                font-family:  "{font_families}"; 
                font-size: 12pt;
            }}
        </style>
        """

        result = f"""
        {css_style}
        {html_str}
        """
        return result
