from projen.awscdk import AwsCdkPythonApp

project = AwsCdkPythonApp(
    author_email="rneljan@gmail.com",
    author_name="ArJSarmiento",
    cdk_version="2.1.0",
    module_name="llama_index_in_lambda",
    name="llama_index_in_lambda",
    poetry=True,
    version="0.1.0",
)

project.synth()