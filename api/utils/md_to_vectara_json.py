import json
import re
import os

from MarkdownFrontmatterExtractor import MarkdownFrontmatterExtractor
from ContentCleaner import ContentCleaner

# removes import lines and replace names.product with vectara
def process_line(line):
    line = re.sub(r'<Config\s+v="names\.product"\s*/?>', "Vecrata", line)
    return line


def md_to_vectara_json(md_file):
    with open(md_file, 'r') as file:
        content = file.read()

    frontmatter_extractor = MarkdownFrontmatterExtractor(md_file)
    frontmatter_params = frontmatter_extractor.extract()
    print(frontmatter_params)

    # eleminate unwated content
    cleaner = ContentCleaner()
    content = cleaner.clean_content(content)
    
    # Initialize the JSON structure
    vectara_json = {
        "documentId": frontmatter_params['id'],
        "title": frontmatter_params['title'],
        "metadataJson": "", 
        "section": []
    }
    
    # Regex to find headers (## or higher) and their content
    lines = content.split('\n')
    current_section = {}
    first_section = None
    current_subsections = []
    is_header_found = False

    
    for line in lines:
        line = process_line(line)
        

        if line is None:
            continue
        header_match = re.match(r'(#{2,})\s+(.+)', line)
        
        if header_match:
            is_header_found = True
            header_level = len(header_match.group(1))  # number of hashes indicates the level
            header_title = header_match.group(2)
            
            if header_level == 2:  # Section
                # If there's a current section, append it before creating a new one
                if current_section:
                    if current_subsections:
                        current_section["section"] = current_subsections
                    vectara_json["section"].append(current_section)
                
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

        elif not is_header_found :
            
            if first_section:
                first_section["text"] += line.strip() + " "
            else:
                first_section = {
                    "title": frontmatter_params['title'],
                    "text": line.strip()
                }
                vectara_json["section"].append(first_section)
            

    # Append any remaining section after the loop
    if current_section:
        if current_subsections:
            current_section["section"] = current_subsections
        vectara_json["section"].append(current_section)

    # Create output file name based on input, adding "_vectara" before file extension
    base_name, ext = os.path.splitext(md_file)
    output_file = f"{base_name}_vectara.json"

    # Save the JSON output to a file
    with open(output_file, 'w') as json_file:
        json.dump(vectara_json, json_file, indent=4)

    print(f"Conversion completed! JSON saved to {output_file}")

if __name__ == "__main__":
    import sys

    # Check if the user provided a markdown file as an argument
    if len(sys.argv) != 2:
        print("Usage: python md_to_vectara_json.py <markdown_file>")
    else:
        md_to_vectara_json(sys.argv[1])
        
# Example usage:
# md_to_vectara_json("input.md")
