from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from pypdf import PdfReader

# ---------------------------------
# LOAD MODEL
# ---------------------------------

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

# ---------------------------------
# STORAGE
# ---------------------------------

documents = []
chunks = []

# ---------------------------------
# DOCUMENT FOLDER
# ---------------------------------

folder_path = "data/documents"

# ---------------------------------
# TEXT CHUNKER
# ---------------------------------

def chunk_text(text, chunk_size=500):

    words = text.split()

    chunked = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunked.append(chunk)

    return chunked

# ---------------------------------
# CHECK IF FOLDER EXISTS
# ---------------------------------

if os.path.exists(folder_path):

    # ---------------------------------
    # READ DOCUMENTS
    # ---------------------------------

    for filename in os.listdir(folder_path):

        filepath = os.path.join(
            folder_path,
            filename
        )

        text = ""

        # TXT / MD FILES

        if filename.endswith(".txt") or filename.endswith(".md"):

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

        # PDF FILES

        elif filename.endswith(".pdf"):

            reader = PdfReader(filepath)

            for page in reader.pages:

                extracted = page.extract_text()

                if extracted:

                    text += extracted + "\n"

        # ---------------------------------
        # CHUNK DOCUMENT
        # ---------------------------------

        if text.strip():

            text_chunks = chunk_text(text)

            for chunk in text_chunks:

                chunks.append(chunk)

                documents.append({

                    "filename": filename,

                    "content": chunk

                })

# ---------------------------------
# CREATE VECTOR DATABASE
# ---------------------------------

if len(chunks) > 0:

    embeddings = model.encode(

        chunks,

        convert_to_numpy=True

    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(embeddings)
    )

else:

    index = None

# ---------------------------------
# SEARCH FUNCTION
# ---------------------------------

def search_documents(query, top_k=4):

    if index is None:

        return "No training documents found."

    query_embedding = model.encode(

        [query],

        convert_to_numpy=True

    )

    distances, indices = index.search(

        np.array(query_embedding),

        top_k

    )

    results = []

    for idx in indices[0]:

        if idx < len(documents):

            results.append(

                documents[idx]["content"]

            )

    return "\n\n".join(results)