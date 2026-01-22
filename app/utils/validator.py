import tldextract
from datetime import datetime

class NewsValidator:
    def __init__(self):
        # In production, these would be loaded from a database or external API
        self.trusted_domains = ["reuters.com", "apnews.com", "bbc.co.uk", "nytimes.com"]
        self.flagged_domains = ["dailybuzz.fake", "worldnews-scam.net"]

    def validate_source(self, url: str) -> dict:
        """
        Returns a source reputation score.
        """
        if not url:
            return {"score": 0.5, "status": "unknown"}
            
        extracted = tldextract.extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}"
        
        if domain in self.trusted_domains:
            return {"score": 1.0, "status": "trusted"}
        elif domain in self.flagged_domains:
            return {"score": 0.0, "status": "blacklisted"}
        
        return {"score": 0.5, "status": "neutral"}

    def check_recency(self, publish_date: str) -> bool:
        # Real-time fake news often uses very old stories out of context
        # Check if the news is more than 3 years old
        try:
            p_date = datetime.strptime(publish_date, "%Y-%m-%d")
            return (datetime.now() - p_date).days < 1095
        except:
            return True # Fallback if no date is provided