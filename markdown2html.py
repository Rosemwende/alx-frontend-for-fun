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
    # Handle headers
    header_match = re.match(r"^(#{1,6}) (.+)", line)
    if header_match:
        header_level = len(header_match.group(1))
        return f"<h{header_level}>{header_match.group(2)}</h{header_level}>", in_list

    # Handle list items
    list_match = re.match(r"^[-*] (.+)", line)
    if list_match:
        return f"<li>{list_match.group(1)}</li>", True

    # Replace bold (**text**) and emphasis (__text__), handle nesting
    while "**" in line or "__" in line:
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)  # Bold
        line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)    # Emphasis

    # Handle MD5 hash syntax [[text]]
    line = re.sub(
        r"\[\[(.+?)\]\]",
        lambda match: hashlib.md5(match.group(1).encode()).hexdigest(),
        line,
    )

    # Handle text transformations ((text))
    line = re.sub(
        r"\(\((.+?)\)\)",
        lambda match: re.sub(r"[cC]", "", match.group(1)),
        line,
    )

    # Treat remaining text as a paragraph
    return f"<p>{line}</p>", False

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

                # Skip empty lines
                if not line:
                    if in_list:
                        html_lines.append("</ul>")
                        in_list = False
                    continue

                # Process the Markdown line
                html_line, list_detected = process_markdown_line(line, in_list)

                # Handle opening/closing list tags
                if list_detected:
                    if not in_list:
                        html_lines.append("<ul>")
                        in_list = True
                else:
                    if in_list:
                        html_lines.append("</ul>")
                        in_list = False

                html_lines.append(html_line)

            # Close any open list at the end
            if in_list:
                html_lines.append("</ul>")

        # Write to the output HTML file
        with open(output_file, "w") as html_file:
            html_file.write("\n".join(html_lines))

    except FileNotFoundError:
        sys.stderr.write(f"Error: {input_file} does not exist\n")
        sys.exit(1)

if __name__ == "__main__":
    # Check the number of arguments
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py <input_file> <output_file>\n")
        sys.exit(1)

    # Extract input and output file names
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Perform the conversion
    markdown_to_html(input_file, output_file)
