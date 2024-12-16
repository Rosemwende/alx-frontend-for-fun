#!/usr/bin/python3
"""
Markdown to HTML converter script
"""

import sys
import re
import hashlib

def process_markdown_line(line):
    """Converts a single line of Markdown to HTML."""
    heading_match = re.match(r'^(#{1,6}) (.+)', line)
    if heading_match:
        level = len(heading_match.group(1))
        content = heading_match.group(2)
        return f"<h{level}>{content}</h{level}>"

    if line.startswith('- '):
        content = line[2:].strip()
        return f"<li>{content}</li>", 'ul'

    if line.startswith('* '):
        content = line[2:].strip()
        return f"<li>{content}</li>", 'ol'

    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)

    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

    line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)

    line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(2).replace('c', '').replace('C', ''), line)

    line = line.replace('\n', '<br/>')

    return f"<p>{line.strip()}</p>"

def convert_markdown_to_html(input_file, output_file):
    """Converts a Markdown file to an HTML file."""
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            in_list = False
            list_type = ''

            for line in infile:
                line = line.rstrip()
                if not line:
                    if in_list:
                        outfile.write(f"</{list_type}>\n")
                        in_list = False
                        list_type = ''
                    continue

                result = process_markdown_line(line)

                if isinstance(result, tuple):
                    html_line, current_list_type = result
                    if not in_list:
                        outfile.write(f"<{current_list_type}>\n")
                        in_list = True
                        list_type = current_list_type
                    outfile.write(f"{html_line}\n")
                else:
                    if in_list:
                        outfile.write(f"</{list_type}>\n")
                        in_list = False
                        list_type = ''
                    outfile.write(f"{result}\n")

            if in_list:
                outfile.write(f"</{list_type}>\n")
    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point for the script."""
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)

if __name__ == "__main__":
    main()
