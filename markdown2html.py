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


def main():
    """Main function to handle the arguments and conversion"""
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(input_file, output_file)
    sys.exit(0)


if __name__ == "__main__":
    main()
