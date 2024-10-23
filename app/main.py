from fastapi import FastAPI, Query
from search import hybrid_results

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/search")
async def search(query: str = Query(..., description="The search query")):
    hybrid_results_df, synthesized_response = hybrid_results(query)
    hybrid_results_json = hybrid_results_df.to_dict(orient="records")
   
    return {
        "hybrid_results": hybrid_results_json,
        "synthesized_response": {
            "thought_process": synthesized_response.thought_process,
            "answer": synthesized_response.answer,
        }
    }