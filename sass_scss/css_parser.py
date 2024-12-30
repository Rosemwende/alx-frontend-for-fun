#!/usr/bin/python3
import re

class CSSParser():
    
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        if self.file_path is None:
            return False
        
        with open(self.file_path, "r") as file:
            file_content = file.read()

        if not file_content:
            return False

        # Cleanup
        file_content = self.__remove_comments(file_content)
        file_content = self.__remove_newline(file_content)
        
        # Parsing
        self.__parse(file_content)
        return self.selectors

    def __remove_comments(self, s):
        return re.sub(r"/\*.*?\*/", "", s, flags=re.DOTALL)

    def __remove_newline(self, s):
        return s.replace("\n", "")

    def __remove_extra_spaces(self, s):
        return re.sub(r"\s+", " ", s).strip()

    def __clean_key(self, s):
        return s.strip()

    def __parse(self, s):
        self.selectors = {}
        for block in s.split("}"):
            if "{" in block:
                selector, properties = block.split("{")
                selector = self.__clean_key(selector)
                properties = self.__parse_properties(properties)
                self.selectors[selector] = properties

    def __parse_properties(self, properties_str):
        properties = {}
        for prop in properties_str.split(";"):
            if ":" in prop:
                name, value = prop.split(":", 1)
                properties[self.__clean_key(name)] = self.__remove_extra_spaces(value)
        return properties

    def validate_property(self, selector, property_name, expected_value):
        selector_data = self.selectors.get(selector)
        if not selector_data:
            return False
        return selector_data.get(property_name) == expected_value


if __name__ == "__main__":
    css_parser = CSSParser("test.css")
    selectors = css_parser.parse()

    print("Selectors Parsed:", selectors)

    button_valid = css_parser.validate_property("button", "color", "#FF0000")
    hover_valid = css_parser.validate_property("button:hover", "color", "#00FF00")

    print("Button color valid:", button_valid)
    print("Button:hover color valid:", hover_valid)
