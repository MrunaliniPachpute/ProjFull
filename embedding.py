import os

import faiss
from sentence_transformers import SentenceTransformer

from config.settings import *

from services.database_service import DatabaseService
from services.embedding_cache import EmbeddingCache
from services.knowledge_base import KnowledgeBase


print("=" * 60)
print("Loading Oracle Data")
print("=" * 60)

db = DatabaseService()

complaints = db.get_closed_complaints()
acks = db.get_acknowledgements()

db.close()

print(f"Resolved Complaints : {len(complaints)}")
print(f"Acknowledgements   : {len(acks)}")
print()

print("=" * 60)
print("Building Knowledge Base")
print("=" * 60)

kb = KnowledgeBase().build(
    complaints,
    acks
)

# ---------------- EMPTY KB CHECK ---------------- #

if kb.empty:

    print("No valid conversations found.")
    print("Knowledge Base not created.")
    exit()

# ---------------- REMOVE EMPTY RECORDS ---------------- #

kb = kb.dropna(
    subset=[
        "conversation",
        # "ai_resolution"
    ]
)

kb = kb[
    kb["conversation"].astype(str).str.strip() != ""
]

# kb = kb[
#     kb["ai_resolution"].astype(str).str.strip() != ""
# ]

kb = kb.reset_index(drop=True)

if kb.empty:

    print("Knowledge Base is empty after cleaning.")
    exit()

print(f"Knowledge Base Size : {len(kb)}")
print()

# ---------------- BUILD EMBEDDING TEXT ---------------- #

texts = []

for _, row in kb.iterrows():

    text = f"""
Subject:
{row['subject']}

Complaint:
{row['complaint']}

Priority:
{row['priority']}

Department:
{row['department']}

Conversation:
{row['conversation']}

"""

    texts.append(text.strip())

print("=" * 60)
print("Loading Embedding Model")
print("=" * 60)

model = SentenceTransformer(MODEL_NAME)

print()

print("=" * 60)
print("Generating Embeddings")
print("=" * 60)

embeddings = model.encode(

    texts,

    show_progress_bar=True,

    convert_to_numpy=True

)

embeddings = embeddings.astype("float32")

faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print()

print("=" * 60)
print("Saving FAISS Index")
print("=" * 60)

os.makedirs(
    CACHE_FOLDER,
    exist_ok=True
)

faiss.write_index(
    index,
    FAISS_INDEX
)

EmbeddingCache().save_metadata(
    METADATA_FILE,
    kb
)

print()

print("=" * 60)
print("Knowledge Base Created Successfully")
print("=" * 60)

print(f"Indexed Tickets : {len(kb)}")
print(f"Embedding Size  : {dimension}")