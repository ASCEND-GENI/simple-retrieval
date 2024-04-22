# import os
# import PyPDF2
# import openai

# # Set your OpenAI API key
# openai.api_key = 'your_openai_api_key_here'

import os
from dotenv import load_dotenv
# import requests
import json
import time
import copy

load_dotenv()

from openai import OpenAI
import numpy as np
from PyPDF2 import PdfReader
import pickle
import pandas as pd


ASCEND_ORG_ID = os.getenv('ASCEND_ORG_ID')
OPENAI_KEY = os.getenv('SS_OPENAI_API_KEY')

client = OpenAI(
    api_key=OPENAI_KEY,
    organization=ASCEND_ORG_ID,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)


# global total_cost
# total_cost = 0
start_time = time.time()
print("Start time: ", start_time)

emb_model = "text-embedding-3-small"
emb_model = "text-embedding-3-large"
emb_model = "text-embedding-ada-002"


def extract_text_from_pdf(pdf_path) -> list[str]:
    reader = PdfReader(pdf_path)
    return [page.extract_text() for page in reader.pages]

def generate_embedding(text):
    response = client.embeddings.create(
        input=text,
        model=emb_model
    )
    cost = 0
    if emb_model == "text-embedding-3-small": cost += response.usage.total_tokens * 0.02 / 1000000
    elif emb_model == "text-embedding-3-large": cost += response.usage.total_tokens * 0.13 / 1000000
    elif emb_model == "text-embedding-ada-002": cost += response.usage.total_tokens * 0.10 / 1000000

    print("cost: ", cost)
    return (response.data[0].embedding, cost)

def build_vector_database(pdf_folder):
    total_cost = 0

    vector_database = {"Filename": [], "Embedding": [], "Chunk": []}
    for i, filename in enumerate(os.listdir(pdf_folder)):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            text: list[str] = extract_text_from_pdf(pdf_path)
            for j, page in enumerate(text):
                if page == "":
                    continue
                else:
                    # chunk the page text first
                    chunks = [chunk for chunk in text_splitter.split_text(text=page)]
                    for k, chunk in enumerate(chunks):
                        vector_database["Filename"].append(f"{filename}_{j}_{k}")
                        (embedding, cost) = generate_embedding(chunk)
                        total_cost += cost
                        vector_database["Embedding"].append(embedding)
                        vector_database["Chunk"].append(chunk)
                print(f"Processed {filename} page {j}; {j+1}/{len(text)} done; total cost: ${total_cost}")
        elif filename.endswith(".txt"):
            with open(os.path.join(pdf_folder, filename), 'r') as file:
                text = file.read()
                chunks = [chunk for chunk in text_splitter.split_text(text=text)]
                for j, chunk in enumerate(chunks):
                    vector_database["Filename"].append(f"{filename}_{j}")
                    (embedding, cost) = generate_embedding(chunk)
                    total_cost += cost
                    vector_database["Embedding"].append(embedding)
                    vector_database["Chunk"].append(chunk)
                print(f"Processed {filename}; {i+1}/{len(os.listdir(pdf_folder))} done; total cost: ${total_cost}")
        print(f"Processed {filename}; {i+1}/{len(os.listdir(pdf_folder))} done; total cost: ${total_cost}")
    df = pd.DataFrame(vector_database)
    return (df, total_cost)

if __name__ == "__main__":
    pdf_folder = "demo-files/document/nrc"
    (vector_database_df, total_cost) = build_vector_database(pdf_folder)
    vector_database_df.to_pickle("demo-files/emb/pkl/NRC_regulations.pkl")

    vector_database_df.to_csv('demo-files/emb/csv/NRC_regulations.csv', index=False)

    end_time = time.time()
    print("time elapsed: ", end_time - start_time)
    print("Total cost: $", total_cost)
    
    # Now you have a dictionary where keys are PDF filenames and values are embeddings
    # You can use this database for retrieval or further analysis
