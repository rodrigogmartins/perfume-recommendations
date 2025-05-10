from fastapi import FastAPI, HTTPException, Query

from src.perfumes.dto.user_input_query import UserInputQuery
from src.perfumes.get_perfumes_recommendations import get_sorted_perfumes
from src.perfumes.search_perfumes_by_text import search_perfumes_by_text
from src.perfumes.utils.user_query_input_builder import user_input_query_builder

app = FastAPI()


@app.get("/api/perfumes/search")
def search_perfumes(query: str = Query(..., min_length=2), limit: int = 10):
    results = search_perfumes_by_text(query, limit)
    return results

@app.post("/api/perfumes/recommendations")
async def perfumes_recommendations(user_input_query: UserInputQuery):
    try:
        user_input_query = user_input_query_builder(user_input_query)
        perfumes = get_sorted_perfumes(user_input_query)
        return { "items": perfumes }
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Something went wrong")
