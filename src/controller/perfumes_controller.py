from fastapi import HTTPException, Query, APIRouter

from src.utils.format_perfume_id import format_perfumes_ids
from src.perfumes.dto.user_input_query import UserInputQuery
from src.perfumes.get_perfumes_recommendations import get_sorted_perfumes
from src.perfumes.list_perfumes_ordered_by_name import list_perfumes_ordered_by_name
from src.perfumes.search_perfumes_by_text import search_perfumes_by_text
from src.perfumes.utils.user_query_input_builder import user_input_query_builder
from src.infra.logger import setup_logger

router = APIRouter()
logger = setup_logger("perfumes_controller")

@router.get("/perfumes/search")
def search_perfumes(
    query: str = Query(None),
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0)
):
    try:
        logger.info(f"Search - Querying perfumes with filters. Query: {query}, Limit: {limit}, Offset: {offset}")
        perfumes = list_perfumes_ordered_by_name(limit, offset) \
            if (query == "") or (query is None) \
            else search_perfumes_by_text(query, limit, offset)

        result = { "items": format_perfumes_ids(perfumes) }
        logger.info(f"Search - Search result: {result}")
        return result
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/perfumes/recommendations")
async def perfumes_recommendations(
    user_input_query: UserInputQuery,
    limit: int = Query(10, ge=1, le=10)
):
    try:
        logger.info(f"Recommendations - Raw filters: {user_input_query} limit: {limit}")
        user_input_query = user_input_query_builder(user_input_query)

        logger.info(f"Recommendations - Querying perfumes with parsed filters: {user_input_query}")
        perfumes = get_sorted_perfumes(user_input_query, limit)
        result = { "items": format_perfumes_ids(perfumes) }

        logger.info(f"Recommendations - Recommendations result: {result}")
        return result
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went wrong")
