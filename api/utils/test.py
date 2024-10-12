import markdown

# Read MD file
with open('query-corpus.api.mdx', 'r') as f:
    text = f.read()

# Convert to HTML
html = markdown.markdown(text)
print(html)