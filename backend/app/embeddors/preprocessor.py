import nltk
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

nltk_data_dir = os.environ.get("NLTK_DATA", "/tmp/nltk_data")
if not os.path.exists(os.path.join(nltk_data_dir, "corpora", "stopwords")):
    nltk.download("stopwords", download_dir=nltk_data_dir)
nltk.data.path.append(nltk_data_dir)
stemmer = nltk.stem.SnowballStemmer("dutch")
stopwords = nltk.corpus.stopwords.words("dutch")


class Preprocessor:
    @classmethod
    def preprocessing(cls, txt: str) -> str:
        stemmed = stemmer.stem(txt).split()
        filtered_words = [word for word in stemmed if word not in stopwords]
        return " ".join(filtered_words)

    @classmethod
    def combine_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Generate new vectorised column 'embedding' in the dataframe"""
        columns = df.columns
        df["combined_col"] = ""
        for col in columns:
            df["combined_col"] += " - " + df[col]
        return df["combined_col"].str[3:]  # cut off the first ' - '
