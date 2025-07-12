import logging, chromadb
from google.adk.tools import ToolContext
from sentence_transformers import SentenceTransformer
from google.genai.types import Part

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

async def knowledge_base_tool(
    tool_context: ToolContext
) -> dict :
    filename = "text"
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        chroma_client = chromadb.PersistentClient(path="./agent/data/chroma_data/")
        collection_name = "test001"

        query = tool_context.state["user_query"]
        collection = chroma_client.get_collection(name=collection_name)
        query_embedding = model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )
        # 构造上下文内容
        context_parts = []
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            context_parts.append(
                f"[Source {i + 1}] File: {meta.get('file_name', 'unknown')}\n"
                f"Content: {doc}\n"
                f"Relevance score: {1 - results['distances'][0][i]:.2f}\n"
            )

        context_text = "\n".join(context_parts) if context_parts else "No relevant documents found"

        # 存储为 Artifact
        version = await tool_context.save_artifact(
            filename=filename,
            artifact=Part(text=context_text)
        )
        logger.info("Saved artifact %s, ver %i", filename, version)
        return {"status": "OK"}

    except Exception as err:

        logger.error("Failed to append complaint to %s: %s", filename, err)
        return {"status": "ERROR", "error_message": str(err)}
