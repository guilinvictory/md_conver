import markdown


class MarkdownUtils:
    CSS_FOR_TABLE = """
    <!-- CSS for table -->
    <style>
        table, th, td {
            border: 1px solid;
        }
        table {
            width: 100%;
        }
    </style>
    """

    @classmethod
    def convert_markdown_to_html(cls, md_text: str) -> str:
        html = markdown.markdown(text=md_text, extensions=["extra", "toc"])
        return f"""
        {html}
        {cls.CSS_FOR_TABLE}
        """ if "<table>" in html else html

    @staticmethod
    def strip_markdown_wrapper(md_text: str) -> str:
        # removing leading and trailing whitespaces
        md_text = md_text.strip()

        # removing codeblock wrapper if existed
        wrapper = "```"
        if md_text.endswith(wrapper):
            if md_text.startswith(wrapper):
                md_text = md_text[len(wrapper): -len(wrapper)]
            elif md_text.startswith(f"{wrapper}markdown"):
                md_text = md_text[(len(f"{wrapper}markdown")): -len(wrapper)]

        return md_text
