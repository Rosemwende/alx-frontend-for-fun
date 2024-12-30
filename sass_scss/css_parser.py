from bs4 import BeautifulSoup

def parse_css(file_path):
    with open(file_path, 'r') as css_file:
        css_content = css_file.read()

    styles = {}
    for rule in css_content.split('}'):
        if '{' in rule:
            selector, properties = rule.split('{')
            properties_dict = {}
            for prop in properties.split(';'):
                if ':' in prop:
                    key, value = prop.split(':')
                    properties_dict[key.strip()] = value.strip()
            styles[selector.strip()] = properties_dict
    return styles

def check_color(styles, selector, expected_color):
    if selector in styles and 'color' in styles[selector]:
        return styles[selector]['color'] == expected_color
    return False

if __name__ == "__main__":
    file_path = "styles.css"
    expected_color_button = "#FF0000"
    expected_color_hover = "#00FF00"
    
    styles = parse_css(file_path)
    button_result = check_color(styles, "button", expected_color_button)
    hover_result = check_color(styles, "button:hover", expected_color_hover)

    print(f"Button color correct: {button_result}")
    print(f"Button:hover color correct: {hover_result}")
