import concurrent.futures
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.schema import MetadataMode, TextNode
from llama_index.core.node_parser import (
    SentenceSplitter,
    # SemanticSplitterNodeParser
)
from llama_index.embeddings.openai import OpenAIEmbedding
from ai_news.news import News
from ai_news.news.util import Category, NewsArticle
from dotenv import load_dotenv

load_dotenv()


def get_news(
    topic: str = 'artificial intelligence',
    category: Category | None = None,
    country: str | None = None,
    language: str = 'en',
) -> list[NewsArticle]:
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
        list[NewsArticle]: List of articles based on given params.

    """
    news = News()

    # Sources.
    sources = news.get_sources(
        country=country,
        category=category,
        language=language,
    )

    # TODO: Get more than 100 articles.
    articles = news.get_articles(
        q=topic,
        sources=sources,
    )
    return articles


def split_to_nodes(
    splitter: SentenceSplitter,
    articles: list[NewsArticle],
    embed_model: BaseEmbedding | None = None,
) -> list[TextNode]:
    """Split news articles to `list[TextNode]` from `SentenceSplitter`.

    Args:
        splitter (SentenceSplitter): Splitter to use.
        articles (list[NewsArticle]): List of news articles.
        embed_model (BaseEmbedding, optional): Embedding object to use.
            Defaults to None.

    Returns:
        list[TextNode]: Text nodes.

    """

    nodes: list[TextNode] = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        nodes_future = map(
            lambda article: executor.submit(
                _create_nodes,
                article,
                splitter=splitter,
                embed_model=embed_model,
            ),
            articles
        )

        for future in concurrent.futures.as_completed(nodes_future):
            try:
                nodes.extend(future.result())  # type: list[TextNode]
            except Exception as e:
                print(f'{e}')

    return nodes


def _create_nodes(
    article: NewsArticle,
    splitter: SentenceSplitter,
    embed_model: BaseEmbedding | None = None,
) -> list[TextNode]:
    """Create `TextNode`s for a news article."""

    # Note: We return list[TextNode] because an article can be split
    # into multiple chunks.
    nodes: list[TextNode] = []
    for chunk in splitter.split_text(article.content):
        # Create node from article.
        node = TextNode(
            text=chunk,
            extra_info={
                'title': article.title,
                'author': article.author,
                'source': article.source.name,
                'description': article.description,
                'url': article.url,
                'published_at': article.published_at.strftime('%Y-%m-%dT%H:%M:%S'),
                'image_url': article.image_url,
            },
        )

        # Embed node content.
        if embed_model is not None:
            embed_text = node.get_content(metadata_mode=MetadataMode.ALL)
            node_embedding = embed_model.get_text_embedding(
                text=embed_text
            )
            node.embedding = node_embedding
        nodes.append(node)

    return nodes


if __name__ == '__main__':
    from pprint import pprint
    articles = get_news()
    pprint(articles[:3])
    print(f'{len(articles)}')

    splitter = SentenceSplitter()
    embed_model = OpenAIEmbedding()
    nodes = split_to_nodes(splitter, articles, embed_model)
    print(f'Nodes = {len(nodes),}')
    print(nodes[0].get_content(MetadataMode.ALL))
