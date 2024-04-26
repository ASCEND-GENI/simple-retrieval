import chainlit as cl
import os

from retrieval import load_vector_database, generate_embedding, retrieve_chunks, extract_page


# @cl.step
# async def tool(message: cl.Message):
#     # Simulate a running task
#     await cl.sleep(2)

#     current_step = cl.context.current_step

#     print("Message of the step:", message.content)
#     # # Override the input of the step
#     # current_step.input = "My custom input"

#     # # Override the output of the step
#     # current_step.output = "My custom output"

#     return "Response from the tool!"


@cl.step
async def print_gen_emb(cost: float):
    return f"embedding generated, cost: ${str(cost)}"

@cl.step
async def print_ret_chunks():
    await cl.sleep(0.03)
    return "Chunks retrieved!"


@cl.on_chat_start
async def on_chat_start():
    # # Sending a pdf with the local file path
    # elements = [
    #   cl.Pdf(name="pdf1", display="side", path="demo-files/retrieved/calculation of dosage for combination pr.pdf")
    # ]

    # await cl.Message(content="Look at this local pdf1!", elements=elements).send()

    # Load vector database
    vector_database_file = "demo-files/emb/pkl/NRC_regulations.pkl"
    vector_database_df = load_vector_database(vector_database_file)

    cl.user_session.set("vdb_df", vector_database_df)

    print("A new chat session has started!")


@cl.on_message
async def main(message: cl.Message):
    query_embedding, cost = await generate_embedding(message.content)
    await print_gen_emb(cost)

    # Retrieve chunks using cosine similarity
    retrieval_results = await retrieve_chunks(query_embedding, cl.user_session.get("vdb_df"))
    await print_ret_chunks()

    filename = message.content[:40]
    new_dir_path = f"demo-files/retrieved/{filename}"
    os.mkdir(new_dir_path)
    extract_page([key for key, chunk, similarity in retrieval_results[:20]], f"{new_dir_path}/{filename}", cl.user_session.get("vdb_df"))

    # Sending a pdf and txt with the local file path
    # elements = [
    #     cl.Pdf(name="pdf", display="side", path="demo-files/retrieved/calculation of dosage for combination pr.pdf")
    # ]

    elements = [
        cl.Pdf(name="pdf", display="side", path=f"{new_dir_path}/{filename}.pdf"),
        cl.File(name="txt", display="side", path=f"{new_dir_path}/{filename}.txt"),
    ]

    # await cl.Message(content="This message has a txt", elements=elements).send()
    await cl.Message(content="Look at this local txt and pdf!", elements=elements).send()

    # # Send the final answer.
    # await cl.Message(content="This is the final answer").send()


@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")

