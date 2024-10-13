import re

class MarkdownFrontmatterExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.frontmatter = {}

    def read_markdown_file(self):
        """Read the Markdown file and return its content."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            raise ValueError(f"File not found: {self.file_path}")

    def extract_frontmatter_params(self, md_content):
        frontmatter_match = re.search(r'---\n(.*?)\n---', md_content, re.DOTALL)

        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            params = {}
            patterns = {
                'id': r'id:\s*(\S+)',
                'title': r'title:\s*(.+)',
                'pagination_label': r'pagination_label:\s*(.+)',
                'sidebar_label': r'sidebar_label:\s*(.+)',
                'sidebar_position': r'sidebar_position:\s*(\d+)',
                'sidebar_class_name': r'sidebar_class_name:\s*(.+)',
                'sidebar_custom_props': r'sidebar_custom_props:\s*(.+)',
                'displayed_sidebar': r'displayed_sidebar:\s*(.+)',
                'hide_title': r'hide_title:\s*(true|false)',
                'hide_table_of_contents': r'hide_table_of_contents:\s*(true|false)',
                'toc_min_heading_level': r'toc_min_heading_level:\s*(\d+)',
                'toc_max_heading_level': r'toc_max_heading_level:\s*(\d+)',
                'pagination_next': r'pagination_next:\s*(.+)',
                'pagination_prev': r'pagination_prev:\s*(.+)',
                'parse_number_prefixes': r'parse_number_prefixes:\s*(true|false)',
                'custom_edit_url': r'custom_edit_url:\s*(.+)',
                'keywords': r'keywords:\s*(.+)',
                'description': r'description:\s*(.+)',
                'image': r'image:\s*(.+)',
                'slug': r'slug:\s*(.+)',
                'tags': r'tags:\s*(.+)',
                'draft': r'draft:\s*(true|false)',
                'unlisted': r'unlisted:\s*(true|false)',
                'last_update': r'last_update:\s*(.+)',
            }

            # Extract values using regex patterns
            for key, pattern in patterns.items():
                match = re.search(pattern, frontmatter)
                if match:
                    # Handle boolean values
                    if key in ['hide_title', 'hide_table_of_contents', 'draft', 'unlisted', 'parse_number_prefixes']:
                        params[key] = match.group(1).lower() == 'true'
                    elif key in ['sidebar_position', 'toc_min_heading_level', 'toc_max_heading_level']:
                        params[key] = int(match.group(1))
                    else:
                        params[key] = match.group(1)

            self.frontmatter = params  # Store the extracted frontmatter in the instance variable

        else:
            raise ValueError("Markdown file missing frontmatter")

    def get_frontmatter(self):
        """Return the extracted frontmatter parameters."""
        return self.frontmatter

    def extract(self):
        """Main method to extract frontmatter from the markdown file."""
        md_content = self.read_markdown_file()
        self.extract_frontmatter_params(md_content)
        return self.get_frontmatter()
