import json
import re
import os
from .MarkdownFrontmatterExtractor import MarkdownFrontmatterExtractor
from .ContentCleaner import ContentCleaner

class MarkdownToVectaraConverter:
    def __init__(self, md_file):
        self.md_file = md_file
        self.frontmatter_extractor = MarkdownFrontmatterExtractor(md_file)
        self.cleaner = ContentCleaner()
        self.vectara_json = {}

    def process_line(self, line):
        return re.sub(r'<Config\s+v="names\.product"\s*/?>', "Vectara", line)

    def extract_frontmatter(self):
        return self.frontmatter_extractor.extract()

    def clean_content(self, content):
        return self.cleaner.clean_content(content)

    def convert(self):
        with open(self.md_file, 'r') as file:
            content = file.read()

        frontmatter_params = self.extract_frontmatter()
        print(frontmatter_params)

        content = self.clean_content(content)

        # Initialize the JSON structure
        self.vectara_json = {
            "documentId": frontmatter_params['id'],
            "title": frontmatter_params['title'],
            "metadataJson": "", 
            "section": []
        }

        self.parse_content(content, frontmatter_params['title'])

        return json.dumps(self.vectara_json, indent=4)  # Return JSON as a string

    def parse_content(self, content, default_title):
        lines = content.split('\n')
        current_section = {}
        first_section = None
        current_subsections = []
        is_header_found = False

        for line in lines:
            line = self.process_line(line)

            if line is None:
                continue
            header_match = re.match(r'(#{2,})\s+(.+)', line)

            if header_match:
                is_header_found = True
                header_level = len(header_match.group(1))  # number of hashes indicates the level
                header_title = header_match.group(2)

                if header_level == 2:  # Section
                    if current_section:
                        if current_subsections:
                            current_section["section"] = current_subsections
                        self.vectara_json["section"].append(current_section)

                    current_section = {
                        "title": header_title,
                        "section": []
                    }
                    current_subsections = []

                elif header_level == 3 and current_section:  # Subsection
                    subsection = {
                        "title": header_title,
                        "text": ""
                    }
                    current_subsections.append(subsection)

            elif current_section and line.strip():  # Append text to section or subsection
                if current_subsections:
                    current_subsections[-1]["text"] += line.strip() + " "
                else:
                    current_section["text"] = current_section.get("text", "") + line.strip() + " "

            elif not is_header_found:
                if first_section:
                    first_section["text"] += line.strip() + " "
                else:
                    first_section = {
                        "title": default_title,
                        "text": line.strip()
                    }
                    self.vectara_json["section"].append(first_section)

        # Append any remaining section after the loop
        if current_section:
            if current_subsections:
                current_section["section"] = current_subsections
            self.vectara_json["section"].append(current_section)

if __name__ == "__main__":
    import sys

    # Check if the user provided a markdown file as an argument
    if len(sys.argv) != 2:
        print("Usage: python md_to_vectara_json.py <markdown_file>")
    else:
        converter = MarkdownToVectaraConverter(sys.argv[1])
        json_output = converter.convert()
        print(json_output)  # Print the JSON output
