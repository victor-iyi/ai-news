from typing import Any
from enum import Enum, auto

from chromadb.api import ClientAPI
from chromadb import EphemeralClient, PersistentClient, HttpClient

from llama_index.core import StorageContext, VectorStoreIndex
# from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.embeddings.utils import EmbedType
from llama_index.core.schema import TextNode
from llama_index.vector_stores.chroma import ChromaVectorStore


class ClientType(Enum):
    """Chroma DB client type."""
    LOCAL = auto()
    IN_MEMORY = auto()
    HTTP_CLIENT = auto()
    CLOUD_CLIENT = auto()


def get_client(
    *,
    client_type: ClientType,
    **kwargs: Any,
) -> ClientAPI:
    """Get Chroma Client based on ClientType.

    Args:
        connection_type (ConnectionType): Type of client to use.

    Kwargs:
        Appropriate keyword arguments for the choosen client type.

    Returns:
        ClientAPI: Chroma client.

    """
    match client_type:
        case ClientType.LOCAL:
            db = PersistentClient(**kwargs)
        case ClientType.IN_MEMORY:
            db = EphemeralClient(**kwargs)
        case ClientType.HTTP_CLIENT:
            db = HttpClient(**kwargs)
        case ClientType.CLOUD_CLIENT:
            raise NotImplementedError('CloudClient not yet supported.')
        case _:
            raise ValueError('Invalid ConnectionType.')

    return db


def create_index(
    client: ClientAPI,
    collection_name: str,
    nodes: list[TextNode] | None = None,
    embed_model: EmbedType | None = None,
) -> VectorStoreIndex:
    """Create or load VectorStoreIndex from Chroma.

    Args:
        client (ClientAPI): Chroma client.
        collection_name (str): Name of chroma collection.
        nodes (list[TextNode], optional): List of text node.
            Defaults to None.
        embed_model (EmbedType, optional): `BaseEmbedding` or embedding str to use.
            Defaults to None.

    Returns:
        VectorStoreIndex: Created or loaded vector store index.

    """
    # Create new collection if it doesn't exist.
    collection = client.get_or_create_collection(name=collection_name)

    # Create storage context from chroma vector store.
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if nodes is not None:
        # Create from nodes
        index = VectorStoreIndex(
            nodes=nodes,
            embed_model=embed_model,
            storage_context=storage_context,
            show_progress=True,
        )
    else:
        # Load from vector store.
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embed_model,
            storage_context=storage_context,
        )

    return index


if __name__ == '__main__':
    from pprint import pprint
    from ai_news.rag.data import get_news, split_to_nodes
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.embeddings.openai import OpenAIEmbedding

    client = get_client(
        client_type=ClientType.LOCAL,
        path='res/vector_store',
    )

    collection_name = 'artificial_intelligence'

    # Check if collection exists.
    collection_exists = False
    if any(collection.name == collection_name for collection in client.list_collections()):
        collection_exists = True

    if not collection_exists:
        articles = get_news()
        pprint(articles[:3])
        print(f'Num articles: {len(articles)}')

        splitter = SentenceSplitter()
        nodes = split_to_nodes(splitter, articles)
    else:
        nodes = None

    index = create_index(
        client=client,
        collection_name=collection_name,
        nodes=nodes,
        embed_model=OpenAIEmbedding(),
    )
    print(index)
