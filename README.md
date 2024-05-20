# Simple Retrieval

...

## Python Environment Setup

To create a Python environment, you can use the following command:

```bash
python[version] -m venv venv
source venv/bin/activate
pip install -r requirements.txt
...
pip freeze -> requirements.txt
```

## Neo4j

```bash
MATCH (n)-[r]->(m) RETURN n, r, m
```
