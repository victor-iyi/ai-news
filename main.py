from pprint import pprint

from ai_news.news import Category, News


def main() -> None:
    """Starting point."""

    news = News()
    category = Category.TECHNOLOGY
    country = None
    language = 'en'

    # Sources.
    sources = news.get_sources(
        country=country,
        category=category,
        language=language,
    )
    pprint(sources)
    print(f'There are {len(sources)} sources given {category=}, {country=}, {language=}')

    print(f'\n{"--" * 50}\n')

    # Top headlines.
    headlines = news.get_top_headlines(
        sources=None,
    )
    pprint(headlines[:3])
    print(f'There are {len(headlines)} headlines')

    print(f'\n{"--" * 50}\n')

    # Everything.
    articles = news.get_articles(
        q='artificial intelligence',
        sources=sources,
    )
    pprint(articles[:3])
    print(len(articles))

    article = articles[0]
    print(f'{article.title=}')
    print(f'{article.author=}')
    print(f'{article.source=}')
    print(f'{article.description=}')
    print(f'{article.content=}')
    print(f'{article.url=}')
    print(f'{article.image_url=}')
    print(f'{article.published_at=}')


if __name__ == '__main__':
    main()
