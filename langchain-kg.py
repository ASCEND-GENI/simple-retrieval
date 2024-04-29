import getpass
import os
import time

# os.environ["OPENAI_API_KEY"] = getpass.getpass()

# Uncomment the below to use LangSmith. Not required.
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
# os.environ["LANGCHAIN_TRACING_V2"] = "true"

import os

from langchain_community.graphs import Neo4jGraph

# os.environ["NEO4J_URI"] = "bolt://localhost:7687"
# os.environ["NEO4J_USERNAME"] = "neo4j"
# os.environ["NEO4J_PASSWORD"] = "password"

start_time = time.time()

graph = Neo4jGraph()



# * * * === * * * === #



import os

from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4-0125-preview",
    organization=os.getenv('ASCEND_ORG_ID'),
    api_key=os.getenv('SS_OPENAI_API_KEY'),
)

llm_transformer = LLMGraphTransformer(llm=llm)


# Now we can pass in example text and examine the results.
from langchain_core.documents import Document

text = """
Marie Curie, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris.
"""
documents = [Document(page_content=text)]
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print(f"Nodes:{graph_documents[0].nodes}")
print(f"Relationships:{graph_documents[0].relationships}")


# # Note that the graph construction process is non-deterministic since we are using LLM. Therefore, you might get slightly different results on each execution.

# # Additionally, you have the flexibility to define specific types of nodes and relationships for extraction according to your requirements.
# llm_transformer_filtered = LLMGraphTransformer(
#     llm=llm,
#     allowed_nodes=["Person", "Country", "Organization"],
#     allowed_relationships=["NATIONALITY", "LOCATED_IN", "WORKED_AT", "SPOUSE"],
# )
# graph_documents_filtered = llm_transformer_filtered.convert_to_graph_documents(
#     documents
# )
# print(f"Nodes:{graph_documents_filtered[0].nodes}")
# print(f"Relationships:{graph_documents_filtered[0].relationships}")

graph.add_graph_documents(graph_documents)

end_time = time.time()
print(f"Time taken: {end_time - start_time:.2f}s")