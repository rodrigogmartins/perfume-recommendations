from fastapi import FastAPI, HTTPException

from src.perfumes.dto.user_input_query import UserInputQuery
from src.perfumes.get_perfumes import get_sorted_perfumes
from src.perfumes.utils.user_query_input_builder import user_input_query_builder

app = FastAPI()

@app.post("/api/perfumes/recommendations")
async def perfumes_recommendations(user_input_query: UserInputQuery):
    try:
        user_input_query = user_input_query_builder(user_input_query)
        perfumes = get_sorted_perfumes(user_input_query)
        return { "items": perfumes }
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Something went wrong")
