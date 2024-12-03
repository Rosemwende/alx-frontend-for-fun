#!/usr/bin/python3
import sys
import os
import markdown


def markdown_to_html(input_file, output_file):
    """Converts a markdown file to an HTML file"""
    try:
        with open(input_file, 'r') as md_file:
            md_content = md_file.read()

        html_content = markdown.markdown(md_content)

        with open(output_file, 'w') as html_file:
            html_file.write(html_content)

    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
	sys.exit(1)
