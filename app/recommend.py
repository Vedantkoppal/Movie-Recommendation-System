import faiss
import numpy as np
import os

basedir = os.path.abspath(os.path.dirname(__file__))
index_file_path = os.path.join(basedir,"Data/processed/faiss_index_file.idx")

index = faiss.read_index(index_file_path)
def recommedfinal(indices_to_reconstruct):
    reconstructed_vectors = np.array([index.reconstruct(idx) for idx in indices_to_reconstruct])
    distances, indices = index.search(reconstructed_vectors, 10)
    flat_indices = indices.ravel()
    flat_distances = distances.ravel()
    sort_order = np.lexsort((flat_distances, flat_indices))
    sorted_indices = flat_indices[sort_order]
    unique_indices, unique_pos = np.unique(sorted_indices, return_index=True)
    filtered_indices = [idx for idx in unique_indices.tolist() if idx not in indices_to_reconstruct]
    return filtered_indices


