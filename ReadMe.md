To see how many chunks we have in every collection:
python - <<'PY'
import chromadb
c = chromadb.PersistentClient(path="/app/chroma_db")
for col in c.list_collections():
    x = c.get_collection(col.name)
    print(f"{col.name}: {x.count()} chunks")
PY



To see every chunk that i have: (for axample in the wiki memories collection)

python - <<'PY'
import chromadb

client = chromadb.PersistentClient(path="/app/chroma_db")
col = client.get_collection("wiki_memories")
data = col.get(include=["documents", "metadatas"])

docs = data.get("documents", [])
metas = data.get("metadatas", [])
ids = data.get("ids", [])

print(f"Total chunks: {len(docs)}\n")
for i, (doc, meta, cid) in enumerate(zip(docs, metas, ids), 1):
    source = (meta or {}).get("source")
    chunk = (meta or {}).get("chunk")
    print(f"=== #{i} id={cid} source={source} chunk={chunk} ===")
    print(doc or "")
    print()
PY





To delete a chunk based on ID:

python - <<'PY'
import chromadb
chunk_id = ""
client = chromadb.PersistentClient(path="/app/chroma_db")
col = client.get_collection("wiki_memories")
col.delete(ids=[chunk_id])
print("Deleted:", chunk_id)
PY