import os
from dotenv import load_dotenv
# import requests
import json
import time
import copy

load_dotenv()

from openai import OpenAI
import numpy as np
import PyPDF2
import pickle

from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

ASCEND_ORG_ID = os.getenv('ASCEND_ORG_ID')
OPENAI_KEY = os.getenv('SS_OPENAI_API_KEY')

client = OpenAI(
    api_key=OPENAI_KEY,
    organization=ASCEND_ORG_ID,
)

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


emb_model = "text-embedding-3-small"
emb_model = "text-embedding-3-large"
emb_model = "text-embedding-ada-002"


# Load vector database from file
def load_vector_database(file_path):
    return pd.read_pickle(file_path)

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

# Function to retrieve chunks using cosine similarity
def retrieve_chunks(query_embedding, vector_database_df: pd.DataFrame, threshold=0.7, top_k=10):
    results = []
    for index, row in vector_database_df.iterrows():
        embedding = row['Embedding']
        similarity = cosine_similarity([query_embedding], [embedding])[0][0]
        if similarity >= threshold:
            # print(row)
            # print(row.Filename, row.Filename.Chunk, similarity)
            # print(row.array)
            # print(row.index)
            # print(list(row.index))
            # print(row.get("Filename"))
            results.append((row.get("Filename"), row.get("Chunk"), similarity))
    results.sort(key=lambda x: x[2], reverse=True)
    return results

def extract_page(keys, output_path, df: pd.DataFrame):
    writer = PyPDF2.PdfWriter()
    txt_file = open(f"{output_path}.txt", "w")
    
    for rank, key in enumerate(keys):
        key_parts = key.split("_")
        path = key_parts[0]
        page_number = int(key_parts[1])
        # print(path, page_number)
        if path.endswith(".pdf"):
            reader = PyPDF2.PdfReader(f'demo-files/files/nrc/{path}') # TODO: inefficient to open the file for each page
            writer.add_page(reader.pages[page_number])
        elif not path.endswith(".pdf"):
            txt_file.write(f'***Rank {rank+1}***\nPreviuos Chunk - {path}_{page_number-1}:\n')
            if page_number != 0:
                prev_chunk = df.loc[df['Filename'] == f'{path}_{page_number-1}', 'Chunk'].values[0]
                txt_file.write(f'{prev_chunk}')
            chunk = df.loc[df['Filename'] == key, 'Chunk'].values[0]
            txt_file.write(f'\n\n\nThis Chunk - {key}:\n{chunk}\n\n\nNext Chunk - {path}_{page_number+1}:\n')
            try:
                next_chunk = df.loc[df['Filename'] == f'{path}_{page_number+1}', 'Chunk'].values[0]
                txt_file.write(f'{next_chunk}\n\n\n')
            except:
                pass

            # print(86, chunk)
            # packet = io.BytesIO()
            # can = canvas.Canvas(packet, pagesize=letter)
            # can.drawString(10, 100, str(chunk))
            # can.save()

            # # move to the beginning of the StringIO buffer
            # packet.seek(0)

            # # create a new PDF with Reportlab
            # new_pdf = PyPDF2.PdfReader(packet)
            # # add the "watermark" (which is the new pdf) on the existing page
            # new_page = PyPDF2.PageObject.create_blank_page(width=400, height=600)
            # new_page.merge_page(new_pdf.pages[0])
            # writer.add_page(new_page)
            # # # finally, write "output" to a real file
            # # output_stream = open("destination.pdf", "wb")
            # # output.write(output_stream)
            # # output_stream.close()

            # # # If it's not a PDF file, add text_info to the PDF writer
            # # page = PyPDF2.PageObject.create_blank_page(width=200, height=200)
            # # page.merge_page("just testing")
            # # writer.add_page(page)

    txt_file.close()
    with open(f'{output_path}.pdf', 'wb') as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    # Load vector database
    vector_database_file = "demo-files/emb/pkl/NRC_regulations.pkl"
    vector_database_df = load_vector_database(vector_database_file)

    # Example query embedding
    query = input("Enter the query: ")
    query_embedding, cost = generate_embedding(query)

    print("Cost: $", cost)

    # Retrieve chunks using cosine similarity
    retrieval_results = retrieve_chunks(query_embedding, vector_database_df)
    extract_page([key for key, chunk, similarity in retrieval_results[:20]], f"demo-files/retrieved/{query[:40]}", vector_database_df)

#     # Print retrieval results
#     for i, (key, chunk, similarity) in enumerate(retrieval_results[:20]):
#         print(f'''
# {i} {key}
# {similarity}
# {chunk}
# ''')


# calculation of dosage for combination product