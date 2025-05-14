from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.controller.format_perfume_id import format_perfumes_ids
from src.perfumes.dto.user_input_query import UserInputQuery
from src.perfumes.get_perfumes_recommendations import get_sorted_perfumes
from src.perfumes.list_perfumes_ordered_by_name import list_perfumes_ordered_by_name
from src.perfumes.search_perfumes_by_text import search_perfumes_by_text
from src.perfumes.utils.user_query_input_builder import user_input_query_builder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/perfumes/search")
def search_perfumes(
    query: str = Query(None),
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0)
):
    perfumes = list_perfumes_ordered_by_name(limit, offset) \
        if (query == "") or (query is None) \
        else search_perfumes_by_text(query, limit)

    return { "items": format_perfumes_ids(perfumes) }

@app.post("/api/perfumes/recommendations")
async def perfumes_recommendations(
    user_input_query: UserInputQuery,
    limit: int = Query(10, ge=1, le=10)
):
    try:
        user_input_query = user_input_query_builder(user_input_query)
        perfumes = get_sorted_perfumes(user_input_query, limit)
        return { "items": format_perfumes_ids(perfumes) }
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Something went wrong")
