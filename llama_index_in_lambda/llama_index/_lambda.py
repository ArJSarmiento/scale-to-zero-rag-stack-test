from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration,
    CfnOutput,
)


class RagAPI(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        # Call the base class constructor
        super().__init__(scope, construct_id, **kwargs)

        function_role = iam.Role(
            self,
            "ServerlessRAGAPIRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        # Attach additional policies directly to the role
        function_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:*",  # Allows invoking Amazon Bedrock models
                    "secretsmanager:*",
                ],
                resources=["*"],  # You can specify more granular resource ARNs
            )
        )

        llama_index_lambda = _lambda.DockerImageFunction(
            self,
            "ServerlessRAGAPI",
            code=_lambda.DockerImageCode.from_image_asset(
                "llama_index_in_lambda/llama_index",
                exclude=["*.pyc", ".pytest_cache", "__pycache__", "_lambda.py"],
            ),
            architecture=_lambda.Architecture.X86_64,
            timeout=Duration.seconds(300),
            memory_size=256,
            environment={
                "AWS_LWA_INVOKE_MODE": "response_stream",
            },
            role=function_role,
        )
        lambda_function_url = llama_index_lambda.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            invoke_mode=_lambda.InvokeMode.RESPONSE_STREAM,
        )

        CfnOutput(
            self,
            "LambdaFunctionRootUrl",
            value=lambda_function_url.url,
            description="Root URL to invoke Lambda Function",
        )

        CfnOutput(
            self,
            "LambdaFunctionDocsUrl",
            value=f"{lambda_function_url.url}docs",
            description="Documentation URL to invoke Lambda Function",
        )
