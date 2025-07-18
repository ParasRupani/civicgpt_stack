from pydantic import BaseModel, AnyUrl, Field
from typing import Optional

class NewsArticle(BaseModel):
    """
    Represents a validated news article parsed from an RSS feed.
    Ensures clean data structure before downstream storage or analysis.
    """
    title: str = Field(..., description="The headline or title of the news article.")
    summary: Optional[str] = Field(None, description="A short summary or excerpt of the article.")
    link: AnyUrl = Field(..., description="The direct URL to the full article.")
    published: Optional[str] = Field(None, description="The article's published timestamp as a string.")
    source: Optional[str] = Field(None, description="The RSS feed URL the article was retrieved from.")
    id: Optional[str] = Field(None, description="A unique hash ID derived from the article link.")
