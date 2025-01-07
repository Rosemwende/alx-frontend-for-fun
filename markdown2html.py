#!/usr/bin/python3
"""
Markdown to HTML converter
"""
import sys
import re
import hashlib

def process_markdown_line(line, in_list):
    """
    Process a single line of Markdown to HTML
    """
    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        header_level = len(header_match.group(1))
        content = header_match.group(2)
        content = replace_markdown_syntax(content)
        return f"<h{header_level}>{content}</h{header_level}>", in_list

    list_match = re.match(r"^[-*] (.+)", line)
    if list_match:
        content = replace_markdown_syntax(list_match.group(1))
        return f"<li>{content}</li>", True

    line = replace_markdown_syntax(line)

    return f"<p>{line}</p>", False

def replace_markdown_syntax(line):
    """
    Improve Markdown syntax:
    - Bold
    - Emphasis
    - MD5 Hashing
    - Text transformations
    """
    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)
    line = re.sub(
        r"\[\[(.+?)\]\]",
        lambda match: hashlib.md5(match.group(1).encode()).hexdigest(),
        line,
    )
    line = re.sub(
        r"\(\((.+?)\)\)",
        lambda match: re.sub(r"[cC]", "", match.group(1)),
        line,
    )
    return line

def markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to an HTML file
    """
    in_list = False
    html_lines = []

    try:
        with open(input_file, "r") as md_file:
            for line in md_file:
                line = line.rstrip()

                if not line:
                    if in_list:
                        html_lines.append("</ul>")
                        in_list = False
                    continue

                html_line, list_detected = process_markdown_line(line, in_list)

                if list_detected:
                    if not in_list:
                        html_lines.append("<ul>")
                        in_list = True
                else:
                    if in_list:
                        html_lines.append("</ul>")
                        in_list = False

                html_lines.append(html_line)
            if in_list:
                html_lines.append("</ul>")

        with open(output_file, "w") as html_file:
            html_file.write("\n".join(html_lines))

    except FileNotFoundError:
        sys.stderr.write(f"Error: {input_file} does not exist\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py <input_file> <output_file>\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    markdown_to_html(input_file, output_file)
