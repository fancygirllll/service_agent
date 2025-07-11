import os, time, chromadb, fitz
from sentence_transformers import SentenceTransformer
from docx import Document

# 初始化 Sentence-Transformer 模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 初始化 Chroma 客户端
client = chromadb.PersistentClient(path="chroma_data/")

# 指定文件夹路径
folder_path = 'upload_data/'
collection_name = "test001"

# 检查集合是否存在
existing_collections = client.list_collections()
if collection_name in existing_collections:
    collection = client.get_collection(collection_name)
    print(f"集合 '{collection_name}' 已存在，使用现有集合。")
else:
    collection = client.create_collection(collection_name)
    print(f"集合 '{collection_name}' 不存在，已创建新集合。")

# 读取不同类型文件内容
def extract_text_from_file(filepath):
    if filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    elif filepath.endswith('.docx'):
        doc = Document(filepath)
        return '\n'.join([p.text for p in doc.paragraphs])
    elif filepath.endswith('.pdf'):
        doc = fitz.open(filepath)
        return '\n'.join([page.get_text() for page in doc])
    else:
        return None

# 遍历文件夹处理文件
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    if not os.path.isfile(filepath):
        continue

    if not (filename.endswith('.txt') or filename.endswith('.pdf') or filename.endswith('.docx')):
        print(f"跳过不支持的文件类型：{filename}")
        continue

    text_data = extract_text_from_file(filepath)
    if not text_data:
        print(f"无法读取文件内容：{filename}")
        continue

    text_embeddings = model.encode(text_data)
    timestamp_id = str(int(time.time())) + "_" + filename  # 唯一ID避免冲突

    collection.add(
        documents=[text_data],
        embeddings=[text_embeddings],
        metadatas=[{"source": filename}],
        ids=[timestamp_id]
    )

    print(f"已上传：{filename}")

print("全部文件上传完成")
