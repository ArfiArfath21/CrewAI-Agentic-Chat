import os

import weaviate
from crewai.tools import BaseTool
from crewai.tools.structured_tool import CrewStructuredTool
from typing import Type, List, Dict
from pydantic import BaseModel, Field
from weaviate.classes.config import Configure
from weaviate.classes.query import MetadataQuery

vectorizer_config = Configure.Vectorizer.text2vec_ollama(  # Configure the Ollama embedding integration
    api_endpoint="http://host.docker.internal:11434",
    model=os.getenv("EMBEDDING_MODEL"),  # The model to use
)

def weaviate_client():
    print("Connecting to Weaviate...")
    host = os.getenv("WEAVIATE_HOST", "localhost")
    secure = os.getenv("WEAVIATE_SECURE", False)
    client = weaviate.connect_to_custom(
        http_host=host,
        http_port=os.getenv("WEAVIATE_PORT", 8080),
        http_secure=secure,
        grpc_host=host,
        grpc_port=os.getenv("WEAVIATE_GRPC_PORT", 50051),
        grpc_secure=secure
    )

    print("Weavite client is ready: ", client.is_ready())
    return client


class WeaviateToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    query: str = Field(..., description="Query text to be used for querying the documents.")
    count: int = Field(default=3, description="Number of documents to return in the response.")


def hybrid_query(collection, query: str, limit: int = 3, score: bool = False):
    response = collection.query.hybrid(
        query=query,
        limit=limit,
        return_metadata=MetadataQuery(score=score),
        return_properties=["product_name", "description"]
    )
    print("Response IDs: ", [o.uuid for o in response.objects])
    return response


def query_run(query: str, count: int) -> List[Dict]:
    # Implementation goes here

    # TODO: Switch to a real/stable Weaviate client
    print("Fetching products for query: ", query)
    print("Number of products to return: ", count)

    client = weaviate_client()
    collections = client.collections.list_all()
    print(collections.keys())

    collection = client.collections.get("Products")
    response = hybrid_query(collection, query, limit=3, score=False)

    client.close()
    return [{o.uuid: o.properties} for o in response.objects]


def create_weaviate_tool():
    print("Creating WeaviateProductSearchTool...")
    return CrewStructuredTool.from_function(
        name="WeaviateProductSearchTool",
        description="This tool searches for `count` number of semantically similar products to a `query` in a Weaviate vector database.",
        func=query_run,
        args_schema=WeaviateToolInput,
    )

def get_object_by_id(collection, id: str):
    object = collection.query.fetch_object_by_id(id)
    if object is None:
        return None
    return object.uuid, object.properties

if __name__ == "__main__":
    response = query_run("Samsung Galaxy Smart Phone", 5)