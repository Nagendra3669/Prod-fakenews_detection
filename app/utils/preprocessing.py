import re
import unicodedata

class TextPreprocessor:
    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""
        
        # 1. Normalize unicode (handles weird characters/emojis)
        text = unicodedata.normalize('NFKC', text)
        
        # 2. Remove HTML Tags
        text = re.sub(r'<.*?>', '', text)
        
        # 3. Clean URLs (We might want to keep the URL for validator, 
        # but for text analysis, we replace them with a token)
        text = re.sub(r'http\S+|www\S+|https\S+', '[URL]', text, flags=re.MULTILINE)
        
        # 4. Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    @staticmethod
    def get_word_count(text: str) -> int:
        return len(text.split())