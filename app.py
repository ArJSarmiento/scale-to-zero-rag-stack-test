import os
from aws_cdk import App, Environment
from llama_index_in_lambda.app import MyStack

# for development, use account/region from cdk cli
dev_env = Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="us-east-1")

app = App()
MyStack(app, "llama-index-in-lambda-dev", env=dev_env)
# MyStack(app, "llama-index-in-lambda-prod", env=prod_env)

app.synth()
