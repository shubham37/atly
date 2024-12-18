import re
import unicodedata


def generate_slug(text: str) -> str:
    """
    Generate a slug from a given text.

    Args:
        text (str): Input text to convert to a slug.

    Returns:
        str: The generated slug.
    """
    # Normalize the text to remove accents
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    # Convert to lowercase
    text = text.lower()

    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)

    # Strip leading/trailing hyphens
    text = text.strip('-')

    return text
