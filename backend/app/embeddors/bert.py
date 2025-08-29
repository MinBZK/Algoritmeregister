import os
import torch
import random
from dotenv import load_dotenv
from .preprocessor import Preprocessor
import pandas as pd

os.environ["HF_HOME"] = os.environ.get(
    "HF_HOME", "/tmp/transformers_data"
)  # noqa: E402
from transformers import AutoTokenizer, AutoModel  # noqa: E402

load_dotenv()
# Set a random seed
random_seed = 42
random.seed(random_seed)
torch.manual_seed(random_seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(random_seed)

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"


class Embeddor:
    def __init__(self, model_id: str):
        print(f"loading model: {model_id}")
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModel.from_pretrained(self.model_id)
        self.modelsize = self.model.config.hidden_size

    def embed_query(self, content: str) -> list[float]:
        processed_text = Preprocessor.preprocessing(content)
        encoded_input = self.tokenizer(
            [processed_text], padding=True, truncation=True, return_tensors="pt"
        )
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self._mean_pooling(
            model_output, encoded_input["attention_mask"]
        )
        return sentence_embeddings[0].tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if os.environ.get("CI"):
            return []
        return [self.embed_query(item) for item in texts]

    def embed_df(self, df, cols) -> pd.DataFrame:
        """Generate vectorised column in the dataframe"""
        df["combined_col"] = Preprocessor.combine_df(df[cols])
        df["embedding"] = self.embed_documents(df["combined_col"].tolist())
        return df

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[
            0
        ]  # First element of model_output contains all token embeddings
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )
