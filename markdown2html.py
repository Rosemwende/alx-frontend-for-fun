#!/usr/bin/python3
"""
Markdown to HTML converter
"""

import sys
import re


def process_markdown_line(line):
    """
    Processes a line of Markdown to convert it to the corresponding HTML
    """
    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        level = len(header_match.group(1))
        content = header_match.group(2)
        return f"<h{level}>{content}</h{level}>"

    list_match = re.match(r"^- (.+)", line)
    if list_match:
        return f"<li>{list_match.group(1)}</li>", "list"

    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)

    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)

    line = line.replace("\n", "<br/>\n")

    return f"<p>{line}</p>", "paragraph"


def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to an HTML file
    """
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            list_open = False

            for line in infile:
                line = line.strip()
                if not line:
                    continue

                result, line_type = process_markdown_line(line)

                if line_type == "list":
                    if not list_open:
                        outfile.write("<ul>\n")
                        list_open = True
                    outfile.write(result + "\n")
                else:
                    if list_open:
                        outfile.write("</ul>\n")
                        list_open = False
                    outfile.write(result + "\n")

            if list_open:
                outfile.write("</ul>\n")

    except FileNotFoundError:
        print(f"Error: {input_file} does not exist.", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Main entry point of the script
    """
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)


if __name__ == "__main__":
    main()
