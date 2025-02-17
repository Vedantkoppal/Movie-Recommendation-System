from qdrant_client.http import models
from app import qdrant,app

def recommend_qdrant(indices_to_reconstruct, qdrant_client = qdrant, collection_name = app.config['QDRANT_COLLECTION_NAME']):
    # Fetch vectors from Qdrant
    query_results = qdrant_client.retrieve(
        collection_name=collection_name,
        ids=indices_to_reconstruct,
        with_vectors=True
    )

    # Extract vectors & perform batch similarity search
    search_results = qdrant_client.search_batch(
        collection_name=collection_name,
        requests=[
            models.SearchRequest(vector=res.vector, limit=10) for res in query_results
        ]
    )

    # Extract and sort indices
    flat_results = [(point.id, point.score) for batch in search_results for point in batch]
    flat_results.sort(key=lambda x: (x[0], x[1]))  # Sort by index, then distance

    # Remove duplicates while preserving order
    unique_indices = list(dict.fromkeys(idx for idx, _ in flat_results))

    # Filter out input indices
    return [idx for idx in unique_indices if idx not in indices_to_reconstruct]




# def recommedfinal(indices_to_reconstruct):
#     reconstructed_vectors = np.array([index.reconstruct(idx) for idx in indices_to_reconstruct])
#     distances, indices = index.search(reconstructed_vectors, 10)
#     flat_indices = indices.ravel()
#     flat_distances = distances.ravel()
#     sort_order = np.lexsort((flat_distances, flat_indices))
#     sorted_indices = flat_indices[sort_order]
#     unique_indices, unique_pos = np.unique(sorted_indices, return_index=True)
#     filtered_indices = [idx for idx in unique_indices.tolist() if idx not in indices_to_reconstruct]
#     return filtered_indices
    # pass
# import faiss
# import numpy as np
# import os

# basedir = os.path.abspath(os.path.dirname(__file__))
# index_file_path = os.path.join(basedir,"Data/processed/faiss_index_file.idx")

# index = faiss.read_index(index_file_path)

# using qdrant instead of faiss