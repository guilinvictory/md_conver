import io
import logging
import re
from typing import Generator

import markdown
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from docx import Document
from docx.oxml.ns import qn
from docx.shared import RGBColor
from htmldocx import HtmlToDocx
from xhtml2pdf import pisa

from tools.utils.md_utils import MarkdownUtils
from tools.utils.mimetype_utils import MimeType
from tools.utils.param_utils import get_md_string, get_meta_data


def is_contains_chinese_chars(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def set_chinese_fonts(doc):
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    rPr = style.element.get_or_add_rPr()
    rPr.rFonts.set(qn('w:eastAsia'), '宋体')


def set_font_color_to_black(doc: Document):
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb =  RGBColor(0, 0, 0) # 这会移除任何颜色设置，通常情况下它会是黑色（默认颜色）


    return doc


def to_word(answer):
    html = markdown.markdown(text=answer, extensions=["extra", "toc"])
    new_parser = HtmlToDocx()
    doc: Document = new_parser.parse_html_string(html)
    doc = set_font_color_to_black(doc)
    if is_contains_chinese_chars(html):
        set_chinese_fonts(doc)
    result_bytes_io = io.BytesIO()
    doc.save(result_bytes_io)
    result_file_bytes = result_bytes_io.getvalue()
    return result_file_bytes


def to_pdf(answer):
    html_str = _convert_to_html(answer)
    result_file_bytes = pisa.CreatePDF(
        src=html_str.encode("utf-8"),
        dest_bytes=True,
        encoding="utf-8",
    )
    return result_file_bytes


class MarkdownToDocxTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:

        answer = get_md_string(tool_parameters, is_strip_wrapper=True)
        type_content=tool_parameters.get("type")
        print(type_content)
        try:
            match type_content:
                case "pdf":
                    result_file_bytes = to_pdf(answer)
                    yield self.create_blob_message(
                        blob=result_file_bytes,
                        meta=get_meta_data(
                            mime_type=MimeType.PDF,
                            output_filename=tool_parameters.get("测试文档"),
                        ),
                    )
                case "word":
                    result_file_bytes = to_word(answer)
                    yield self.create_blob_message(
                        blob=result_file_bytes,
                        meta=get_meta_data(
                            mime_type=MimeType.DOCX,
                            output_filename=tool_parameters.get("测试文档"),
                        ),

                    )
                case _:
                    yield self.create_text_message("Failed to convert markdown text to  file ,the type is null ")
        except Exception as e:
            logging.exception("Failed to convert file")
            yield self.create_text_message(f"Failed to convert markdown text to DOCX file, error: {str(e)}")
            return


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