import boto3
import json
from botocore.client import logger
from botocore.exceptions import ClientError

from ai import bedrock_claude_langchain
from utils import prompts, file_reader, extract_table_names


def generate_text(model_id, body):
    logger.info(
        "Generating text with Amazon Titan Text model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    finish_reason = response_body.get("error")

    logger.info(
        "Successfully generated text with Amazon Titan Text model %s", model_id)

    return response_body


def covert_to_spring_boot(filename):
    """print(bedrock_claude_langchain.query_code("Generate business documentation for ","../data_dir/store_proc.txt"))"""
    try:
        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        print("Sending prompt please wait ...")
        # reading from file prompt
        # reading from db prompt
        prompt = prompts.get_spring_boot_prompt("3.3.0",
                                                "17") + "For following Stored Procedure\n" + extract_table_names.get_file_content(
            filename) + " \n" + prompts.get_domain_prompt_from_file(
            filename)
        #return prompt
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000000,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        })

        response_body = generate_text(model_id, body)
        print(response_body["content"][0]["text"])
        return response_body["content"][0]["text"]

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))


