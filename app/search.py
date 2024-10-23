from database.vector_store import VectorStore
from services.synthesizer import Synthesizer

# Initialize VectorStore
vec = VectorStore()

def hybrid_results(query: str):
    # keyword_results = vec.keyword_search(query=query, limit=5)
    # semantic_results = vec.semantic_search(query=query, limit=5)
    hybrid_results = vec.hybrid_search(query=query, keyword_k=5, semantic_k=5)
    response = Synthesizer.generate_response(question=query, context=hybrid_results)
    return hybrid_results, response