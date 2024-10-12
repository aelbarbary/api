import re

class ContentCleaner:
    def eliminate_frontmatter(self, content):
        frontmatter_pattern = r'---\n(.*?)\n---'
        content_without_frontmatter = re.sub(frontmatter_pattern, '', content, count=1, flags=re.DOTALL)
        return content_without_frontmatter.strip()

    def remove_imports(self, content):
        import_pattern = r'import\s*{[^}]*}\s*from\s*["\'][^"\']*["\'];?'
        cleaned_content = re.sub(import_pattern, '', content)
        return cleaned_content.strip()

    def remove_topic_buttons(self, content):
        topic_button_pattern = r'<TopicButton[^>]*>.*?</TopicButton>'
        cleaned_content = re.sub(topic_button_pattern, '', content, flags=re.DOTALL)
        return cleaned_content.strip()

    def clean_content(self, content):
        cleaned_content = self.eliminate_frontmatter(content)
        cleaned_content = self.remove_imports(cleaned_content)
        cleaned_content = self.remove_topic_buttons(cleaned_content)
        return cleaned_content.strip()  
