from typing import List

from pydantic import BaseModel


# noinspection PyDataclass
class UserInputQuery(BaseModel):
    ownedPerfumes: List[str] = []
    likedPerfumes: List[str] = []
    notLikedPerfumes: List[str] = []
    likedNotes: List[str] = []
    notLikedNotes: List[str] = []
    likedAccords: List[str] = []
    notLikedAccords: List[str] = []
    dayShifts: List[str] = []
    climates: List[str] = []
    seasons: List[str] = []