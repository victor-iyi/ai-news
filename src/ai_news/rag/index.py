from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

from ai_news.rag.data import (
    get_news,
    split_to_nodes,
)
from ai_news.rag.vector_db import (
    ClientType,
    create_vector_store_index,
    get_client,
)


def create_index(
    topic: str = 'artificial intelligence',
    collection_name: str = 'artificial_intelligence',
) -> VectorStoreIndex:
    """Create index.

    Args:
        collection_name (str, optional): Name of the collection for ChromaDB.
            Defaults to 'artificial_intelligence'.

    Returns:
        VectorStoreIndex: Loaded/created vector index.

    """

    # Get the vector db client.
    client = get_client(
        client_type=ClientType.LOCAL,
        path='res/vector_store',
    )

    # Check if collection exists.
    collection_exists = False
    if any(
        collection.name == collection_name for collection in client.list_collections()
    ):
        collection_exists = True

    if not collection_exists:
        # TODO: Get more than 100 news articles.
        # Get news articles.
        articles = get_news(topic=topic)

        # TODO: Use SemanticSplitterNodeParser.
        # Split articles into list[TextNode].
        splitter = SentenceSplitter()
        nodes = split_to_nodes(splitter, articles)
    else:
        # Load from existing collection in the vector db.
        nodes = None

    # Create VectorStoreIndex.
    index: VectorStoreIndex = create_vector_store_index(
        client=client,
        collection_name=collection_name,
        nodes=nodes,
        embed_model=OpenAIEmbedding(),
    )

    return index


if __name__ == '__main__':
    index = create_index(collection_name='artificial_intelligence')
    print(index)
