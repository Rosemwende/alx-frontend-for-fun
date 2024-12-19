#!/usr/bin/python3
"""
Markdown to HTML converter
"""

import sys
import re


def process_markdown_line(line, list_open):
    """
    Process a single line of Markdown into corresponding HTML
    """
    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        level = len(header_match.group(1))
        content = header_match.group(2)
        content = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content)
        content = re.sub(r"__(.+?)__", r"<em>\1</em>", content)
        return f"<h{level}>{content}</h{level}>", "header", list_open

    list_match = re.match(r"^[-*] (.+)", line)
    if list_match:
        content = list_match.group(1)
        content = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content)
        content = re.sub(r"__(.+?)__", r"<em>\1</em>", content)
        if not list_open:
            return f"<ul>\n<li>{content}</li>", "list", True
        return f"<li>{content}</li>", "list", list_open

    if list_open:
        return "</ul>", "close_list", False

    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)
    return f"<p>{line}</p>", "paragraph", list_open


def convert_markdown_to_html(input_file, output_file):
    """
    Convert Markdown file to HTML file
    """
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            list_open = False

            for line in infile:
                line = line.strip()
                if not line:
                    continue

                converted_line, line_type, list_open = process_markdown_line(line, list_open)

                if line_type == "close_list":
                    outfile.write(converted_line + "\n")
                else:
                    outfile.write(converted_line + "\n")

            if list_open:
                outfile.write("</ul>\n")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Entry point of the script. Validates input arguments
    """
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)


if __name__ == "__main__":
    main()
