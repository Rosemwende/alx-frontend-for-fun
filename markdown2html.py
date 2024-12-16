#!/usr/bin/python3
"""
A script to convert Markdown files to HTML
"""
import sys
import os
import re

def parse_markdown_to_html(input_file, output_file):
    try:
        with open(input_file, 'r') as md_file:
            lines = md_file.readlines()

        html_lines = []
        in_list = False
        list_type = None

        for line in lines:
            line = line.rstrip()

            heading_match = re.match(r'^(#{1,6}) (.+)', line)
            if heading_match:
                level = len(heading_match.group(1))
                content = heading_match.group(2)
                html_lines.append(f'<h{level}>{content}</h{level}>')
                continue

            if line.startswith('- '):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                    list_type = 'ul'
                html_lines.append(f'<li>{line[2:]}</li>')
                continue

            if line.startswith('* '):
                if not in_list:
                    html_lines.append('<ol>')
                    in_list = True
                    list_type = 'ol'
                html_lines.append(f'<li>{line[2:]}</li>')
                continue

            if in_list and not (line.startswith('- ') or line.startswith('* ')):
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
   
            line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)

            if line.strip():
                if not html_lines or not html_lines[-1].startswith('<p>'):
                    html_lines.append('<p>')
                else:
                    html_lines[-1] += '<br/>'
                html_lines[-1] += line
            elif html_lines and html_lines[-1].startswith('<p>'):
                html_lines[-1] += '</p>'

        if in_list:
            html_lines.append(f'</{list_type}>')
        if html_lines and html_lines[-1].startswith('<p>') and not html_lines[-1].endswith('</p>'):
            html_lines[-1] += '</p>'

        with open(output_file, 'w') as html_file:
            html_file.write('\n'.join(html_lines) + '\n')

    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    parse_markdown_to_html(input_file, output_file)
