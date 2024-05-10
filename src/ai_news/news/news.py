import os
from newsapi import NewsApiClient
# from newsapi.newsapi_exception import NewsAPIException
from dotenv import load_dotenv
from ai_news.news.util import (
    # Category,
    NewsArticle,
    Source,
)

load_dotenv()


class News:
    def __init__(self) -> None:
        self._client = NewsApiClient(
            api_key=os.environ['NEWS_API_KEY'],
        )

    def get_top_headlines(
        self,
        q: str | None = None,
        qintitle: str | None = None,
        sources: list[Source] | None = None,
        category: str | None = None,
        country: str | None = None,
        language: str = 'en',
    ) -> list[NewsArticle]:
        """

        Args:
            qintitle (str, optional): Keywords or a phrase to search for in the article title and body.
                Defaults to None.
            sources (list[Sources], optional): List of news source objects.
                Defaults to None.

        Raises:
            ValueError: cannot mix country/category with sources param.

        Returns:
            list[NewsArticle]: List of news article objects.

        """
        # if sources is not Nwjne

        # Sources.
        if (sources is not None) and ((country is not None) or (category is not None)):
            raise ValueError(
                'cannot mix country/category param with sources param.'
            )

        result = self._client.get_top_headlines(
            q=q,
            qintitle=qintitle,
            sources=Source.source_ids(sources=sources),
            category=category,
            language=language,
            country=country,
        )

        if result['status'] != 'ok':
            raise Exception('Something went wrong')

        raise NotImplementedError()

    def get_sources(
        self,
        category: str | None = None,
        language: str = 'en',
        country: str | None = None,
    ) -> list[Source]:
        """Get available news sources.

        Args:
            category (str, optional): News category, e.g. business, it, technology.
                Default is None.
            language (str, optional): News language.
                Default is 'en'.
            country (str, optional): Two letter country code. E.g us, au, ...
                Default is None.

        Returns:
            list[Source]: List of all or filtered sources.

        """
        result = self._client.get_sources(
            category=category,
            language=language,
            country=country,
        )

        if result['status'] != 'ok':
            raise Exception('Something went wrong')

        sources: list[Source] = []

        for source in result['sources']:
            if source['language'] != language:
                continue
            if category and source['category'] != category:
                continue
            if country and source['country'] != country:
                continue

            s = Source(
                id=source['id'],
                name=source['name'],
                description=source['description'],
                url=source['url'],
                category=source['category'],
                language=source['language'],
                # category=Category.from_str(source['category']),
            )
            sources.append(s)

        return sources


if __name__ == '__main__':
    from pprint import pprint

    news = News()
    category = 'technology'
    country = 'us'
    language = 'en'

    sources = news.get_sources(
        country=country,
        category=category,
    )

    headlines = news.get_top_headlines(
        sources=sources,
    )

    sources = news.get_sources(country='us', category='technology')
    pprint(sources)
    print(len(sources))
