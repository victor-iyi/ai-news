import concurrent.futures
import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from llama_index.core import Document
from newsapi import NewsApiClient
from trafilatura import extract, fetch_url

from ai_news.news.util import (
    Category,
    NewsArticle,
    Source,
)

load_dotenv()


class NewsException(Exception):
    """Something went wrong with the News API."""


class News:
    """Get news articles, headlines and sources from the News API."""

    def __init__(self) -> None:
        self._client = NewsApiClient(
            api_key=os.environ['NEWS_API_KEY'],
        )

    def get_documents(
        self,
        q: str | None = None,
        qintitle: str | None = None,
        sources: list[Source] | None = None,
        domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        language: str = 'en',
        sort_by: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[Document]:
        """Get and parse news into list of `Document`.

        Notes:
            - See the official [News API documentation](https://newsapi.org/docs/endpoints/everything)
            for search syntax and examples.
            - Use `News.get_sources` to locate these programmatically, or look at the
            `sources index <https://newsapi.org/sources>`.

        Args:
            q (str, optional):Keywords or a phrase to search for in the article title and body.
                Defaults to None.
            qintitle (str, optional): Keywords or a phrase to search for in the article title and body.
                Defaults to None.
            sources (list[Source], optional): A comma-seperated string of identifiers
                for the news sources or blogs you want headlines from.
                See `News.get_sources()` to get sources.
                Defaults to None.
            domains (list[str], optional): A comma-seperated string of domains
                (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search to.
                Defaults to None.
            exclude_domains (list[str], optional): A comma-seperated string of domains
                (eg bbc.co.uk, techcrunch.com, engadget.com) to remove from the results.
                Defaults to None.
            from_date (datetime, optional): A date and optional time for the oldest article allowed.
                The format must conform to ISO-8601 specifically as one of either `%Y-%m-%d`
                (e.g. *2019-09-07*) or `%Y-%m-%dT%H:%M:%S` (e.g. *2019-09-07T13:04:15*).
                Defaults to None.
            to_date (datetime, optional):A date and optional time for the newest article allowed.
                The format must conform to ISO-8601 specifically as one of either `%Y-%m-%d`
                (e.g. *2019-09-07*) or `%Y-%m-%dT%H:%M:%S` (e.g. *2019-09-07T13:04:15*).
                Defaults to None.
            language (str, optional): The 2-letter ISO-639-1 code of the language
                you want to get headlines for.
                Defaults to en.
            sort_by (str, optional): The order to sort articles in.
                See `newsapi.const.sort_method` for the set of allowed values.
                Defaults to None.
            page (int, optional): The number of results to return per page (request).
                Defaults to 20. 100 is the maximum.
            page_size (int, optional): Use this to page through the results if
                the total results found is greater than the page size.

        Returns:
            list[Document]: Parsed articles into `Document`s.

        """
        response = self._get_everything(
            q=q,
            qintitle=qintitle,
            sources=sources,
            domains=domains,
            exclude_domains=exclude_domains,
            from_date=from_date,
            to_date=to_date,
            language=language,
            sort_by=sort_by,
            page=page,
            page_size=page_size,
        )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            documents = executor.map(
                News._create_document,
                response,
            )

        return list(documents)

    def get_articles(
        self,
        q: str | None = None,
        qintitle: str | None = None,
        sources: list[Source] | None = None,
        domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        language: str = 'en',
        sort_by: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[NewsArticle]:
        """Get all news articles.

        Notes:
            - See the official [News API documentation](https://newsapi.org/docs/endpoints/everything)
            for search syntax and examples.
            - Use `News.get_sources` to locate these programmatically, or look at the
            `sources index <https://newsapi.org/sources>`.

        Args:
            q (str, optional):Keywords or a phrase to search for in the article title and body.
                Defaults to None.
            qintitle (str, optional): Keywords or a phrase to search for in the article title and body.
                Defaults to None.
            sources (list[Source], optional): A comma-seperated string of identifiers
                for the news sources or blogs you want headlines from.
                See `News.get_sources()` to get sources.
                Defaults to None.
            domains (list[str], optional): A comma-seperated string of domains
                (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search to.
                Defaults to None.
            exclude_domains (list[str], optional): A comma-seperated string of domains
                (eg bbc.co.uk, techcrunch.com, engadget.com) to remove from the results.
                Defaults to None.
            from_date (datetime, optional): A date and optional time for the oldest article allowed.
                The format must conform to ISO-8601 specifically as one of either `%Y-%m-%d`
                (e.g. *2019-09-07*) or `%Y-%m-%dT%H:%M:%S` (e.g. *2019-09-07T13:04:15*).
                Defaults to None.
            to_date (datetime, optional):A date and optional time for the newest article allowed.
                The format must conform to ISO-8601 specifically as one of either `%Y-%m-%d`
                (e.g. *2019-09-07*) or `%Y-%m-%dT%H:%M:%S` (e.g. *2019-09-07T13:04:15*).
                Defaults to None.
            language (str, optional): The 2-letter ISO-639-1 code of the language
                you want to get headlines for.
                Defaults to en.
            sort_by (str, optional): The order to sort articles in.
                See `newsapi.const.sort_method` for the set of allowed values.
                Defaults to None.
            page (int, optional): The number of results to return per page (request).
                Defaults to 20. 100 is the maximum.
            page_size (int, optional): Use this to page through the results if
                the total results found is greater than the page size.

        Returns:
            list[NewsArticle]: List of all news articles that meets the param criteria.

        """
        response = self._get_everything(
            q=q,
            qintitle=qintitle,
            sources=sources,
            domains=domains,
            exclude_domains=exclude_domains,
            from_date=from_date,
            to_date=to_date,
            language=language,
            sort_by=sort_by,
            page=page,
            page_size=page_size,
        )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            articles = executor.map(
                News._create_news_article,
                response,
            )

        return list(articles)

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
            category (str, optional): News category, e.g. business, it, technology.
                Default is None.
            country (str, optional): Two letter country code. E.g us, au, ...
                Default is None.
            language (str, optional): News language.
                Default is 'en'.

        Raises:
            ValueError: cannot mix country/category with sources param.

        Returns:
            list[NewsArticle]: List of top news article headlines.

        """

        # Sources.
        if (sources is not None) and ((country is not None) or (category is not None)):
            raise ValueError('cannot mix country/category param with sources param.')

        response = self._client.get_top_headlines(
            q=q,
            qintitle=qintitle,
            sources=Source.source_ids(sources=sources),
            category=category,
            language=language,
            country=country,
        )  # {status: ok, totalResult: 0, articles: []}

        if response['status'] != 'ok':
            raise NewsException('Something went wrong')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            articles = executor.map(
                News._create_news_article,
                response['articles'],
            )

        return list(articles)

    def get_sources(
        self,
        category: Category | None = None,
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
            category=str(category) if category else None,
            language=language,
            country=country,
        )

        if result['status'] != 'ok':
            raise NewsException('Something went wrong')

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
                category=Category.from_str(source['category']),
                language=source['language'],
                # category=Category.from_str(source['category']),
            )
            sources.append(s)

        return sources

    def _get_everything(
        self,
        q: str | None = None,
        qintitle: str | None = None,
        sources: list[Source] | None = None,
        domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        language: str = 'en',
        sort_by: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[dict[str, Any]]:
        """Get all news articles."""

        response = self._client.get_everything(
            q=q,
            qintitle=qintitle,
            sources=Source.source_ids(sources=sources),
            domains=','.join(domains) if domains else None,
            exclude_domains=(','.join(exclude_domains) if exclude_domains else None),
            from_param=(
                from_date.strftime('%Y-%m-%dT%H:%M:%S')
                if from_date is not None
                else None
            ),
            to=(to_date.strftime('%Y-%m-%dT%H:%M:%S') if to_date is not None else None),
            language=language,
            sort_by=sort_by,  # TODO: Make into Enum
            page=page,
            page_size=page_size,
        )

        if response['status'] != 'ok':
            raise NewsException('Something went wrong')

        articles: list[dict[str, Any]] = response['articles']
        return articles

    @staticmethod
    def fetch_article_content(url: str) -> str | None:
        """Fetch article contents from URL.

        Args:
            url (str): URL of the article.

        Returns:
            str | None: Markdown content of the url or None if it failed.

        """
        # Download a web page.
        downloaded = fetch_url(url)
        content: str | None = None
        if downloaded is not None:
            # Extract information from HTML.
            content = extract(
                downloaded,
                include_links=True,
            )
        return content

    @staticmethod
    def _create_news_article(article: dict[str, Any]) -> NewsArticle:
        """Create `NewsArticle` object from news article json response."""
        # TODO: Use existing source object with matching name.
        source = Source(
            id=article['source']['id'],
            name=article['source']['name'],
        )

        # TODO: article['content'] doesn't contain the full content
        # Might wanna use BeautifulSoup to parse the article['url'] instead.
        content: str = (
            News.fetch_article_content(
                url=article['url'],
            )
            or article['content']
        )

        news_article = NewsArticle(
            title=article['title'],
            author=article['author'],
            content=content,
            description=article['description'],
            published_at=datetime.fromisoformat(article['publishedAt']),
            source=source,
            url=article['url'],
            image_url=article['urlToImage'],
        )
        return news_article

    @staticmethod
    def _create_document(article: dict[str, Any]) -> Document:
        """Create list of `Document` from news article json response."""
        # TODO: Use existing source object with matching name.
        source = Source(
            id=article['source']['id'],
            name=article['source']['name'],
        )

        # TODO: article['content'] doesn't contain the full content
        # Might wanna use BeautifulSoup to parse the article['url'] instead.
        content: str = (
            News.fetch_article_content(
                url=article['url'],
            )
            or article['content']
        )

        document = Document(
            text=content,
            metadata={  # type: ignore[call-arg]
                'title': article['title'],
                'author': article['author'],
                'source': source.name,
                'description': article['description'],
                'published_at': article['publishedAt'],
                'url': article['url'],
                'image_url': article['urlToImage'],
            },
        )
        return document

    @staticmethod
    def _create_documents_from_articles(articles: list[NewsArticle]) -> list[Document]:
        """Create documents & it's metadata from list of articles."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            documents = executor.map(
                lambda article: Document(
                    text=article.content,
                    metadata={  # type: ignore[call-arg]
                        'title': article.title,
                        'author': article.author,
                        'source': article.source.name,
                        'description': article.description,
                        'url': article.url,
                        'published_at': article.published_at.strftime(
                            '%Y-%m-%dT%H:%M:%S'
                        ),
                        'image_url': article.image_url,
                    },
                ),
                articles,
            )
        return list(documents)
