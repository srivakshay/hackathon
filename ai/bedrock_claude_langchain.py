import boto3
from langchain_aws import ChatBedrock

from utils import file_reader


def query_code(prompt, filename):
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    llm = ChatBedrock(
        client=client, model_id=model_id
    )

    response = llm.invoke(prompt + file_reader.get_data_from_file(filename))

    return response.content
