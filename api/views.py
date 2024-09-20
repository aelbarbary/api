from django.shortcuts import render
from rest_framework import status
import pandas as pd
import boto3
from io import StringIO 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import environ
env = environ.Env()
client = OpenAI(api_key=env("OPENAI_API_KEY"))
from django.http import HttpResponse
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.csv_loader import CSVLoader
os.environ["OPENAI_API_KEY"] = env("OPENAI_API_KEY")
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


model = ChatOpenAI(model="gpt-3.5-turbo")

def fetch_csv_from_s3(bucket_name, object_key, local_file_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, object_key, local_file_name)
    return local_file_name

bucket_name = 'ceo-ign'
object_key = 'Financials.csv'
local_file_name = 'local_file.csv'
fetch_csv_from_s3(bucket_name, object_key, local_file_name)

loader = CSVLoader(file_path=local_file_name)
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(model, prompt_template)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

class Chatbot(APIView):
    def post(self, request):
        prompt = request.data.get('prompt', '')

        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if 'generate file' in prompt.lower():
                return self.handle_file_generation(prompt)
            else:
                response = rag_chain.invoke({"input": prompt})
                return Response({'response': response['answer']}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'hello error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def handle_file_generation(self, prompt):
        extracted_data = rag_chain.invoke({"input": prompt})
        data = extracted_data['answer']
        text_file = StringIO()
        text_file.write(data)
        text_file.seek(0)
        response = HttpResponse(text_file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="generated_data.txt"'
        return response