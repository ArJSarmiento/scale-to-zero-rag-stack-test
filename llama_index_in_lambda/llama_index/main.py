import json
import os
from botocore.exceptions import ClientError

from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.bedrock import Bedrock
from pinecone import Pinecone
from llama_index.embeddings.bedrock import BedrockEmbedding, Models
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


from llama_index.core import VectorStoreIndex
import boto3
import uvicorn


async def prompt(input_text: str):
    # Configuration
    secret_name = "pinecone-api-key"
    region_name = os.getenv("AWS_REGION")

    # Create a Session with AWS
    session = boto3.Session(region_name=region_name)

    # Create a Secrets Manager client using the session
    secrets_client = session.client(service_name="secretsmanager")

    # Retrieve the Pinecone API key from AWS Secrets Manager
    try:
        get_secret_value_response = secrets_client.get_secret_value(
            SecretId=secret_name
        )
        secret_string = get_secret_value_response["SecretString"]
        secret = json.loads(secret_string)
        api_key = secret["apiKey"]
        os.environ["PINECONE_API_KEY"] = api_key
    except ClientError as e:
        raise e

    # Initialize Pinecone
    pc = Pinecone(api_key=api_key)
    pinecone_index = pc.Index("elevate-test")
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    # Initialize the embedding model
    embed_model = BedrockEmbedding(
        model_name=Models.TITAN_EMBEDDING_V2_0.value,
        region_name=region_name,
    )

    # Create a vector store index
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store, embed_model=embed_model
    )

    # Initialize the language model
    llm = Bedrock(
        model="anthropic.claude-v2:1",
        region_name=region_name,
    )

    # Create a query engine
    query_engine = index.as_query_engine(llm=llm, streaming=True)

    # Perform the query
    streaming_response = query_engine.query(input_text)
    for text in streaming_response.response_gen:
        yield text


app = FastAPI()


class Chat(BaseModel):
    prompt: str


@app.post("/api/chat")
def api_chat(chat: Chat):
    return StreamingResponse(prompt(chat.prompt))
