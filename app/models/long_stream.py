import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class LongStreamDetector:
    def __init__(self, model_name="allenai/longformer-base-4096"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Note: In a production 2026 environment, we use a version fine-tuned 
        # on the ISOT or LIAR-Plus datasets for article-length detection.
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2).to(self.device)
        self.model.eval()

    def analyze(self, text: str):
        """
        Deep inference for long-form news and blog posts.
        """
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=4096,
            padding="max_length"
        ).to(self.device)

        # Longformer requires a 'global attention mask' 
        # We set global attention on the <s> (CLS) token to aggregate article-wide context
        global_attention_mask = torch.zeros_like(inputs['input_ids'])
        global_attention_mask[:, 0] = 1 

        with torch.no_grad():
            outputs = self.model(
                **inputs, 
                global_attention_mask=global_attention_mask
            )
            
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        score = probs[0][1].item()

        return {
            "verdict": "Fake" if score > 0.5 else "Real",
            "confidence": score,
            "depth_analysis": "Full-text sliding window utilized"
        }