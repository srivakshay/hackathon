import boto3
from langchain_community.llms import Bedrock
from langchain_community.chat_models import BedrockChat
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

model_id = "anthropic.claude-3-haiku-20240307-v1:0"
client = boto3.client("bedrock-runtime", region_name="us-east-1")

llm = BedrockChat(
    client=client, model_id=model_id
)

response = llm.invoke("hi")

print(response.content)