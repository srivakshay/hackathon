import boto3
import json
from botocore.client import logger
from botocore.exceptions import ClientError

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


def main():
    try:
        model_id = 'amazon.titan-text-premier-v1:0'
        print("Sending prompt please wait ...")
        # reading from file prompt
        """prompt = prompts.get_spring_boot_prompt("3.3.0", "17") + "\n for Stored Procedure\n" + file_reader.get_data_from_file(
            "../data_dir/store_proc.txt") + " \n" + prompts.get_domain_prompt_from_file("../data_dir/store_proc.txt")"""

        # reading from db prompt
        prompt = prompts.get_spring_boot_prompt("3.3.0",
                                                "17") + "\n for Stored Procedure\n" + extract_table_names.get_body_mysql(
            "assignment_week3", "sample1") + " \n" + prompts.get_domain_prompt_from_mysql("assignment_week3","sample1")
        print(prompt)
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 3072,
                "stopSequences": [],
                "temperature": 0.5,
                "topP": 0.9
            }
        })

        response_body = generate_text(model_id, body)
        print(f"Input token count: {response_body['inputTextTokenCount']}")

        for result in response_body['results']:
            print(f"Output text: {result['outputText']}")
            print(f"Completion reason: {result['completionReason']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))


if __name__ == "__main__":
    main()
