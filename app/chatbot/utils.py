import re

def minimal_markdown(text):
    # Convert **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Convert *italic*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text