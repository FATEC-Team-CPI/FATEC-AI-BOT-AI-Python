# S3
import  boto3
import os
from huggingface_hub import InferenceClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

BUCKET_NAME = "meu-bucket"

# Configurações de Caminho e Token
CHROMA_PATH = "./chroma_db"

# Inicialização dos Embeddings (Modelo leve para CPU)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Inicialização do Banco Vetorial
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)