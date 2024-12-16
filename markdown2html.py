#!/usr/bin/python3
"""
A script to convert Markdown files to HTML.
"""

import sys
import os
import re

def parse_markdown_to_html(input_file, output_file):
    """
    Parse a Markdown file and convert it to HTML.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as md_file:
            lines = md_file.readlines()
    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    html_lines = []
    in_list = False
    list_type = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        heading_match = re.match(r'^(#{1,6})\s+(.*)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        if line.startswith('- '):
            if not in_list:
                in_list = True
                list_type = 'ul'
                html_lines.append("<ul>")
            html_lines.append(f"<li>{line[2:]}</li>")
            continue

        if line.startswith('* '):
            if not in_list:
                in_list = True
                list_type = 'ol'
                html_lines.append("<ol>")
            html_lines.append(f"<li>{line[2:]}</li>")
            continue

        if in_list:
            html_lines.append(f"</{list_type}>")
            in_list = False
            list_type = None

        if not line.startswith(('#', '-', '*')):
            line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
            line = line.replace('\n', '<br/>')
            html_lines.append(f"<p>{line}</p>")

    if in_list:
        html_lines.append(f"</{list_type}>")

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write('\n'.join(html_lines))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    parse_markdown_to_html(input_file, output_file)
    sys.exit(0)
