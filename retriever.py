import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class Retriever:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the Retriever with a sentence transformer model and FAISS index.
        
        Args:
            model_name (str): Name of the Hugging Face model to use for embeddings.
        """
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.id_map = {}
    
    def build_index(self, data: pd.DataFrame):
        """
        Build a FAISS index from the provided data.
        
        Args:
            data (pd.DataFrame): Preprocessed data with 'id' and 'text_content' columns.
        """
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.model.encode(data['text_content'].tolist(), show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')
        
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        # Map FAISS indices to data IDs
        self.id_map = dict(enumerate(data['id']))
        print("FAISS index built with {} entries.".format(len(self.id_map)))
    
    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve the top-k most similar entries for a given query.
        
        Args:
            query (str): The query text.
            top_k (int): Number of top results to retrieve.
        
        Returns:
            List of tuples: Each tuple contains the ID and similarity score of a retrieved entry.
        """
        # Generate embedding for the query
        query_embedding = self.model.encode([query], show_progress_bar=False)
        query_embedding = np.array(query_embedding).astype('float32')
        
        # Perform search
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Map indices to original IDs and return results
        results = [(self.id_map[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
        return results


if __name__ == "__main__":
    # File paths
    data_file = "preprocessed_data.csv"
    
    # Load preprocessed data
    print("Loading preprocessed data...")
    data = pd.read_csv(data_file)
    
    # Initialize retriever
    retriever = Retriever()
    
    # Build index
    retriever.build_index(data)
    
    # Example query
    print("\nEnter a query to retrieve similar documents:")
    query = input("Query: ")
    results = retriever.retrieve(query, top_k=5)
    
    # Display results
    print("\nTop Results:")
    for doc_id, score in results:
        row = data[data['id'] == doc_id].iloc[0]
        print(f"ID: {doc_id}, Class: {row['class']}, Score: {score:.4f}")
        print(f"Content: {row['text_content'][:200]}...")
        print("-" * 50)
