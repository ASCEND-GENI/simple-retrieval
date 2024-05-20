import time
import os
from langchain_community.graphs import Neo4jGraph


start_time = time.time()

graph = Neo4jGraph()

# from langchain.chains import GraphCypherQAChain
from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4-0125-preview",
    organization=os.getenv('ASCEND_ORG_ID'),
    api_key=os.getenv('SS_OPENAI_API_KEY'),
)
default_llm = ChatOpenAI(
    temperature=0,
    organization=os.getenv('ASCEND_ORG_ID'),
    api_key=os.getenv('SS_OPENAI_API_KEY'),
)
cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=llm,
    # qa_llm=default_llm, # defulat model "gpt-3.5-turbo"
    qa_llm=llm, # defulat model "gpt-3.5-turbo"
    graph=graph,
    verbose=True,
    return_intermediate_steps=True
)
cypher_chain.invoke("Who is the chemist?")
