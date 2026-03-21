from app.integrations import vectormind_adapter


def test_retrieve_documents_from_vectormind_uses_top_k_10_and_normalizes_chunks(monkeypatch, capsys):
    called = {}

    def fake_retrieve(query, k):
        called["query"] = query
        called["k"] = k
        return {
            "documents": [[
                "tadata: vector search uses embeddings to rank related passages. This sentence should survive.",
                "Second clean sentence. Trailing fragment without closing punctuation",
                123,
            ]]
        }

    monkeypatch.setattr(vectormind_adapter, "retrieve", fake_retrieve)

    result = vectormind_adapter.retrieve_documents_from_vectormind("semantic retrieval")
    stdout = capsys.readouterr().out

    assert called == {"query": "semantic retrieval", "k": 10}
    assert "VECTORMIND RAW RETRIEVED CHUNKS:" in stdout
    assert "tadata: vector search uses embeddings to rank related passages. This sentence should survive." in stdout
    assert result == [
        "This sentence should survive.",
        "Second clean sentence.",
    ]
