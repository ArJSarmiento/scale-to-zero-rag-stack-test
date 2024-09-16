import os
from aws_cdk import Stack
from constructs import Construct
from llama_index_in_lambda.llama_index._lambda import RagAPI


class MyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        rag_api = RagAPI(self, "RagAPI")
