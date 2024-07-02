# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# snippet-start:[python.example_code.bedrock-runtime.InvokeModel_AnthropicClaude]
# Use the native inference API to send a text message to Anthropic Claude.

import boto3
import json

from utils import prompts, file_reader

# from botocore.Exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Claude 3 Haiku.
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

# Define the prompt for the model.
"""prompt = prompts.get_spring_boot_prompt("3.3.0", "17") + "\n for Stored Procedure\n" + file_reader.get_data_from_file(
            "../data_dir/store_proc.txt") + " \n" + prompts.get_domain_prompt_from_file("../data_dir/store_proc.txt")"""
prompts = []
prompts.append( "My name is Akshay")
prompts.append("What is my name")
# Format the request payload using the model's native structure.
for prompt in prompts:
    print(prompt)
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

    except (Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

# Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]
    print(response_text)

# snippet-end:[python.example_code.bedrock-runtime.InvokeModel_AnthropicClaude]