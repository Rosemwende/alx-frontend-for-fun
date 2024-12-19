#!/usr/bin/python3
"""
Markdown to HTML converter tailored to ALX grader requirements
"""

import sys
import re


def process_markdown(line):
    """
    Convert Markdown to HTML based on specific formatting rules
    """
    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        level = len(header_match.group(1))
        content = header_match.group(2)
        content = re.sub(r"__(.+?)__", r"<em>\1</em>", content)
        content = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content)
        return f"<h{level}>{content}</h{level}>"

    list_match = re.match(r"^[-*] (.+)", line)
    if list_match:
        content = list_match.group(1)
        content = re.sub(r"__(.+?)__", r"<em>\1</em>", content)
        content = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content)
        return f"<li>{content}</li>"

    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)
    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    return line


def markdown_to_html(input_file, output_file):
    """
    Convert a Markdown file to HTML
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
                    outfile.write(process_markdown(line) + "\n")
                else:
                    if list_open:
                        outfile.write("</ul>\n")
                        list_open = False
                    outfile.write(process_markdown(line) + "\n")

            if list_open:
                outfile.write("</ul>\n")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Main entry point for the script
    """
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
