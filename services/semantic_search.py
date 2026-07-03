import faiss
from sentence_transformers import SentenceTransformer

from config.settings import *

from services.embedding_cache import EmbeddingCache


class SemanticSearch:

    def __init__(self):

        self.model = SentenceTransformer(MODEL_NAME)

        self.index = faiss.read_index(
            FAISS_INDEX
        )

        self.metadata = EmbeddingCache().load_metadata(
            METADATA_FILE
        )

    def search(self, subject, complaint, top_k=5):

        if self.metadata.empty:

            return []

        top_k = min(
            top_k,
            len(self.metadata)
        )

        query = f"""
Subject:
{subject}

Complaint:
{complaint}
"""

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        embedding = embedding.astype("float32")

        faiss.normalize_L2(embedding)

        scores, ids = self.index.search(
            embedding,
            top_k
        )

        results = []

        seen = set()

        for score, idx in zip(scores[0], ids[0]):

            if idx == -1:
                continue

            row = self.metadata.iloc[idx]

            ticket = row["ticket_no"]

            if ticket in seen:
                continue

            seen.add(ticket)

            result = row.to_dict()

            result["similarity"] = round(
                float(score) * 100,
                2
            )

            results.append(result)

        results.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        return results