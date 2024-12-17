#!/usr/bin/python3
"""
Markdown to HTML converter
"""

import sys
import re


def process_markdown_line(line):
    """
    Processes a single line of Markdown and converts it to HTML
    Returns the converted HTML and the line type (e.g., 'list', 'paragraph')
    """
    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        level = len(header_match.group(1))
        content = header_match.group(2)
        return f"<h{level}>{content}</h{level}>", "header"

    list_match = re.match(r"^- (.+)", line)
    if list_match:
        return f"<li>{list_match.group(1)}</li>", "list"

    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)

    return f"<p>{line}</p>", "paragraph"


def convert_markdown_to_html(input_file, output_file):
    """
    Converts the contents of a Markdown file to an HTML file
    Handles lists, headers, and inline formatting
    """
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            list_open = False

            for line in infile:
                line = line.strip()
                if not line:
                    continue

                converted_line, line_type = process_markdown_line(line)

                if line_type == "list":
                    if not list_open:
                        outfile.write("<ul>\n")
                        list_open = True
                    outfile.write(converted_line + "\n")
                else:
                    if list_open:
                        outfile.write("</ul>\n")
                        list_open = False
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
    Entry point of the script
    Validates input arguments and initiates the Markdown to HTML conversion
    """
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)


if __name__ == "__main__":
    main()
