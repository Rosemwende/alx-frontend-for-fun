def process_markdown_line(line):
    """
    Processes a line of Markdown to convert it to the corresponding HTML
    """
    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        level = len(header_match.group(1))
        content = header_match.group(2)
        content = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content)
        content = re.sub(r"__(.+?)__", r"<em>\1</em>", content)
        return f"<h{level}>{content}</h{level}>", "header"

    list_match = re.match(r"^- (.+)", line)
    if list_match:
        item = list_match.group(1)
        item = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", item)
        item = re.sub(r"__(.+?)__", r"<em>\1</em>", item)
        return f"<li>{item}</li>", "list"

    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)

    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)

    line = line.replace("\n", "<br/>\n")

    return f"<p>{line}</p>", "paragraph"
