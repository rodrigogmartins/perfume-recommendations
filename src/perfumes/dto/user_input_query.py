from typing import List, Optional

from pydantic import BaseModel


# noinspection PyDataclass
class UserInputQuery(BaseModel):
    ownedPerfumes: Optional[List[str]] = []
    likedPerfumes: Optional[List[str]] = []
    notLikedPerfumes: Optional[List[str]] = []
    likedNotes: Optional[List[str]] = []
    notLikedNotes: Optional[List[str]] = []
    likedAccords: Optional[List[str]] = []
    notLikedAccords: Optional[List[str]] = []
    dayShifts: Optional[List[str]] = []
    climates: Optional[List[str]] = []
    seasons: Optional[List[str]] = []