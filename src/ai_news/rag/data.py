from dotenv import load_dotenv
from llama_index.core import Document

from ai_news.news import News
from ai_news.news.util import Category

load_dotenv()


def get_news_documents(
    topic: str = 'artificial intelligence',
    category: Category | None = None,
    country: str | None = None,
    language: str = 'en',
) -> list[Document]:
    """Get list of news articles.

    Args:
        topic (str, optional): Keywords or a phrase to search for in the article title and body.
            Defaults to None.
        category (str, optional): News category, e.g. business, it, technology.
            Default is None.
        country (str, optional): Two letter country code. E.g us, au, ...
            Default is None.
        language (str, optional): News language.
            Default is 'en'.

    Returns:
        list[Document]: Parsed articles based on given params.

    """
    news = News()

    # Sources.
    sources = news.get_sources(
        country=country,
        category=category,
        language=language,
    )

    # TODO: Get more than 100 articles.
    documents: list[Document] = news.get_documents(
        q=topic,
        sources=sources,
    )
    return documents


if __name__ == '__main__':
    from pprint import pprint

    from llama_index.core.node_parser import (
        NodeParser,
        SemanticSplitterNodeParser,
        SentenceSplitter,
    )
    from llama_index.core.schema import MetadataMode

    # Get the news articles.
    documents = get_news_documents()
    pprint(documents[0])
    print(f'{len(documents):,=}')

    # Get node splitter to use.
    USE_SEMANTIC = False
    splitter: NodeParser = (
        SemanticSplitterNodeParser.from_defaults()
        if USE_SEMANTIC
        else SentenceSplitter()
    )

    # Split documents into nodes.
    nodes = splitter.get_nodes_from_documents(
        documents=documents,
        show_progress=True,
    )
    print(f'\nNodes = {len(nodes):,=}')
    print(nodes[0].get_content(MetadataMode.ALL))
