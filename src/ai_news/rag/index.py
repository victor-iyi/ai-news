from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import (
    NodeParser,
    SemanticSplitterNodeParser,
    SentenceSplitter,
)
from llama_index.embeddings.openai import OpenAIEmbedding

from ai_news.rag.data import get_news_documents
from ai_news.rag.vector_db import (
    ClientType,
    create_vector_store_index,
    get_client,
)


def create_index(
    topic: str = 'artificial intelligence',
    collection_name: str = 'artificial_intelligence',
    use_semantic_splitter: bool = False,
) -> VectorStoreIndex:
    """Create index.

    Args:
        topic (str, optional): News topic to get.
            Defaults to "artificial intelligence".
        collection_name (str, optional): Name of the collection for ChromaDB.
            Defaults to 'artificial_intelligence'.
        use_semantic_splitter (bool, optional): Whether to use semnatic node splitter.
            Defaults to False.

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
    if any(collection.name == collection_name for collection in client.list_collections()):
        collection_exists = True

    if not collection_exists:
        # TODO: Get more than 100 news articles.
        # Get news articles.
        print(f'Get news article for {topic}...')
        documents = get_news_documents(topic=topic)

        # Split documents into nodes.
        print(f'Splitting {len(documents):,} documents into nodes...\n')
        splitter = get_splitter(use_semantic=use_semantic_splitter)
        nodes = splitter.get_nodes_from_documents(
            documents=documents,
            show_progress=True,
        )
        print(f'{len(documents):,} parsed into {len(nodes):,} nodes.\n')
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


def get_splitter(use_semantic: bool = False) -> NodeParser:
    """Get the sentence splitter to use.

    Args:
        use_semantic (bool, optional): Whether to use semantic node parser.
            Defaults to False.

    Returns:
        type[NodeParser]: Either `SentenceSplitter` or `SemanticSplitterNodeParser`.

    """
    if use_semantic:
        return SemanticSplitterNodeParser.from_defaults()
    return SentenceSplitter()


if __name__ == '__main__':
    index = create_index(
        collection_name='artificial_intelligence',
        use_semantic_splitter=True,
    )
    print(index)
