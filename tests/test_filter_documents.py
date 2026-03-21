from app.operations.filter_documents import filter_documents


def test_filter_documents_rejects_html_and_navigation_fragments_before_scoring():
    result = filter_documents({
        "query": "vector search embeddings",
        "documents": [
            '<a href="/docs">Vector search embeddings guide</a>',
            "Vector search uses embeddings to compare semantic meaning across documents. This explanatory paragraph should remain eligible for ranking.",
        ],
        "top_k": 3,
    })

    assert result["documents"] == [
        "Vector search uses embeddings to compare semantic meaning across documents. This explanatory paragraph should remain eligible for ranking."
    ]


def test_filter_documents_requires_sentence_structure_and_minimum_word_count():
    result = filter_documents({
        "query": "semantic search chunk ranking",
        "documents": [
            "semantic search chunk ranking words only no sentence punctuation here at all",
            "Semantic search improves retrieval quality.",
            "Semantic search improves retrieval quality by ranking chunks with meaningful explanatory context. This sentence keeps the document eligible.",
        ],
        "top_k": 3,
    })

    assert result["documents"] == [
        "Semantic search improves retrieval quality by ranking chunks with meaningful explanatory context. This sentence keeps the document eligible."
    ]
