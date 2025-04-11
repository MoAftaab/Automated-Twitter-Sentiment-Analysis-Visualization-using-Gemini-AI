from googletrans import Translator
from typing import Tuple, Optional
import asyncio

translator = Translator()

async def translate_text(original_text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Translate text to English and return both translated text and original language.
    
    Args:
        original_text (str): Text to be translated
        
    Returns:
        Tuple[Optional[str], Optional[str]]: (translated_text, original_language)
        Returns (None, None) if translation fails
    """
    try:
        translation = await translator.translate(original_text, dest='en')
        return translation.text, translation.src
    except Exception as e:
        print(f"Translation failed: {str(e)}")
        return None, None

async def main():
    # Test with multiple languages
    test_texts = [
        "贸易战打响了！",  # Chinese
        "La guerra comercial ha comenzado!",  # Spanish
        "La guerre commerciale a commencé!",  # French
        "Der Handelskrieg hat begonnen!"  # German
    ]
    
    for text in test_texts:
        translated, original_lang = await translate_text(text)
        if translated and original_lang:
            print(f"\nOriginal ({original_lang}): {text}")
            print(f"Translated: {translated}")
        else:
            print(f"\nFailed to translate: {text}")

if __name__ == "__main__":
    asyncio.run(main())