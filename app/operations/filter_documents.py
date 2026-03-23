def filter_documents(input_data):
    """
    Pass-through filter: preserves retrieval ranking.
    Only trims to a maximum number of documents.
    """
    docs = input_data.get("documents", [])

    if not isinstance(docs, list):
        return {"documents": [], "scoring": []}

    # Keep top-k only (no re-ranking)
    return {"documents": docs[:1], "scoring": []}
