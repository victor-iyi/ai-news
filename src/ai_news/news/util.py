from dataclasses import dataclass, field
from enum import Enum
from typing import Self
from datetime import datetime


class Category(Enum):
    GENERAL = 'general'
    IT = 'it'
    BUSINESS = 'business'
    TECHNOLOGY = 'technology'
    SPORTS = 'sports'

    @classmethod
    def from_str(cls, cat: str) -> Self:
        raise NotImplementedError()


@dataclass
class Source:
    """Sources for articles, blogs, news articles you want."""

    id: str
    name: str
    url: str
    category: str = field(repr=False)
    description: str = field(repr=False)
    language: str = field(default='en', repr=False)

    @classmethod
    def source_ids(cls, sources: list[Self] | None) -> str | None:
        """Returns a comma-separated list of news sources or None.

        Args:
            sources (list[Source]): List of sources.
                Defaults to None.

        Returns:
            str | None: Comma-sepearated news source ids or none.

        """
        if sources:
            return ','.join([source.id for source in sources])

        return None


@dataclass
class NewsArticle:
    title: str
    description: str = field(repr=False)
    content: str
    author: str
    published_at: datetime
    source: Source
    url: str
    image_url: str
