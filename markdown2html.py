#!/usr/bin/python3
"""
A script to convert a Markdown file to an HTML file
"""

import sys
import os

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
            content = md_file.read()

        html_content = f"<html><body>{content}</body></html>"

        with open(output_file, 'w') as html_file:
            html_file.write(html_content)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)
