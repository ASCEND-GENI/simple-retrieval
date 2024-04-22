# Mon. Apr. 22, 2024

## Notice

- Added a basic RAG system. It extracts a PDF or txt

## Next Steps / TODOs

- [ ] add chainlit frontend to the RAG system
- [ ] add BM25
- [ ] How do we crawl?

## Advice / Hope

- Research Thoughts Update
  - Constructing a Knowledge Base (VDB, KG) -> Analyze Question (Entity, What is Asked)… -> Rerank
  - Research Notes
    - Problems with regards to co-referencing and entity disambiguation are innate to our approach, which is using a Knowledge Graph as the facts to to aid the Information Retrieval (IR) process in the 1st stage or retrieval.
    - Why can’t the GPT-2 paper’s Knowledge Graph be used for Information Retrieval?
    - One paper mentions about extracting a whole paper down to “Idea”, “Method”… can’t we give types to each segment of text?
    - MaxSim tries to find the 
    - Disregard the problem of Entity Disambiguation and co-referencing, treat all of them as potential possibilities
- Process Overview: Vectorize word embeddigns for the known entitites and ambiguous entities. Get top k likely candidates for each model and then query GPT-4 for the passage containing both mentions and ask it which one it likely is. 

