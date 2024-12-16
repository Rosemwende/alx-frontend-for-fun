#!/usr/bin/python3
"""
A script to convert a Markdown file to an HTML file
"""

import sys
import os
import re

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, 'r') as md_file:
            content = md_file.readlines()

        html_lines = []
        in_ulist = False
        in_olist = False

        for line in content:
            line = line.strip()

            heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
            if heading_match:
                if in_ulist:
                    html_lines.append("</ul>")
                    in_ulist = False
                if in_olist:
                    html_lines.append("</ol>")
                    in_olist = False
                heading_level = len(heading_match.group(1))
                heading_text = heading_match.group(2).strip()
                html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")

            elif line.startswith('- '):
                if in_olist:
                    html_lines.append("</ol>")
                    in_olist = False
                if not in_ulist:
                    html_lines.append("<ul>")
                    in_ulist = True
                list_item = line[2:].strip()
                html_lines.append(f"<li>{list_item}</li>")

            elif line.startswith('* '):
                if in_ulist:
                    html_lines.append("</ul>")
                    in_ulist = False
                if not in_olist:
                    html_lines.append("<ol>")
                    in_olist = True
                list_item = line[2:].strip()
                html_lines.append(f"<li>{list_item}</li>")

            else:
                if in_ulist:
                    html_lines.append("</ul>")
                    in_ulist = False
                if in_olist:
                    html_lines.append("</ol>")
                    in_olist = False
                html_lines.append(line)

        if in_ulist:
            html_lines.append("</ul>")
        if in_olist:
            html_lines.append("</ol>")

        html_content = "\n".join(html_lines)

        with open(output_file, 'w') as html_file:
            html_file.write(html_content)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)
