#!/usr/bin/python3
"""
Markdown to HTML converter for ALX requirements
"""

import sys
import re


def process_markdown_line(line):
    """
    Process a single line of Markdown into corresponding HTML
    """
    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        level = len(header_match.group(1))
        content = header_match.group(2)
        content = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content)
        content = re.sub(r"__(.+?)__", r"<em>\1</em>", content)
        return f"<h{level}>{content}</h{level}>"

    list_match = re.match(r"^[-*] (.+)", line)
    if list_match:
        content = list_match.group(1)
        content = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content)
        content = re.sub(r"__(.+?)__", r"<em>\1</em>", content)
        return f"<li>{content}</li>"

    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)
    return f"<p>{line}</p>"


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

                if re.match(r"^[-*] ", line):
                    if not list_open:
                        outfile.write("<ul>\n")
                        list_open = True
                    outfile.write(process_markdown_line(line) + "\n")
                else:
                    if list_open:
                        outfile.write("</ul>\n")
                        list_open = False
                    outfile.write(process_markdown_line(line) + "\n")

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
    Entry point of the script. Validates input arguments.
    """
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)


if __name__ == "__main__":
    main()
