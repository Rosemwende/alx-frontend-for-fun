#!/usr/bin/python3
"""
Markdown to HTML converter with additional syntax support
"""

import sys
import re
import hashlib


def process_markdown_line(line):
    """
    Process a single line of Markdown to HTML
    """
    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)
    line = re.sub(
        r"\[\[(.+?)\]\]",
        lambda match: hashlib.md5(match.group(1).encode()).hexdigest(),
        line,
    )
    line = re.sub(r"\(\((.+?)\)\)", lambda match: re.sub(r"[cC]", "", match.group(1)), line)

    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        header_level = len(header_match.group(1))
        return f"<h{header_level}>{header_match.group(2)}</h{header_level}>"

    list_match = re.match(r"^[-*] (.+)", line)
    if list_match:
        return f"<li>{list_match.group(1)}</li>"

    return f"<p>{line}</p>"


def convert_markdown_to_html(input_file, output_file):
    """
    Convert a Markdown file to an HTML file
    """
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            in_list = False

            for line in infile:
                line = line.strip()
                if not line:
                    continue

                if line.startswith(("-", "*")):
                    if not in_list:
                        outfile.write("<ul>\n")
                        in_list = True
                    outfile.write(process_markdown_line(line) + "\n")
                else:
                    if in_list:
                        outfile.write("</ul>\n")
                        in_list = False
                    outfile.write(process_markdown_line(line) + "\n")

            if in_list:
                outfile.write("</ul>\n")

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Main function to parse command-line arguments and initiate the conversion
    """
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_markdown_to_html(input_file, output_file)


if __name__ == "__main__":
    main()
