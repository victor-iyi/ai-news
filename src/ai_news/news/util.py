from dataclasses import dataclass, field
from enum import Enum
from typing import Self
from datetime import datetime


class Category(Enum):
    """Available categories."""

    BUSINESS = 'business'
    ENTERTAINMENT = 'entertainment'
    GENERAL = 'general'
    HEALTH = 'health'
    SCIENCE = 'science'
    SPORTS = 'sports'
    TECHNOLOGY = 'technology'

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Self | str) -> bool:
        if isinstance(other, str):
            return self.value == other
        return self.value == other.value

    def __ne__(self, other: Self | str) -> bool:
        if isinstance(other, str):
            return self.value != other
        return self.value == other.value

    @classmethod
    def from_str(cls, member: str) -> Self:
        """Convert from a string to Category object."""
        if (category := cls.__members__.get(member.upper())) is not None:
            return category
        raise ValueError(f'No member {member} in {cls}')

    @classmethod
    def to_str(cls, category: Self) -> str:
        """Convert a category object to string."""
        return str(category)


@dataclass
class Source:
    """Sources for articles, blogs, news articles you want."""

    id: str
    name: str
    url: str | None = field(default=None, repr=False)
    category: Category | None = field(default=None, repr=True)
    description: str | None = field(default=None, repr=False)
    language: str = field(default='en', repr=False)

    def __eq__(self, other: Self | str) -> bool:
        if not isinstance(other, Source):
            return NotImplemented

        if isinstance(other, str):
            return self.name == other

        return self.name == other.name  # and self.id == other.id

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
    """News article details."""
    title: str
    author: str
    content: str = field(repr=False)
    description: str = field(repr=False)
    published_at: datetime = field(repr=False)
    source: Source = field(repr=False)
    url: str = field(repr=False)
    image_url: str = field(repr=False)
