import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class ShortStreamDetector:
    def __init__(self, model_name="mrm8488/distilroberta-finetuned-fake-news-detection"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def analyze(self, text: str):
        """
        Fast inference for social media snippets and headlines.
        """
        # Tokenize with truncation to 512 tokens (standard BERT limit)
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Convert logits to probabilities
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        score = probs[0][1].item()  # Probability of being "Fake"
        
        return {
            "verdict": "Fake" if score > 0.5 else "Real",
            "confidence": score,
            "tokens_processed": len(inputs['input_ids'][0])
        }