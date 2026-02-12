from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, text_split, download_embeddings, filter_to_minimal_docs
from pinecone import Pinecone
from pinecone import ServerlessSpec 
from langchain_pinecone import PineconeVectorStore

load_dotenv()


PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


extracted_data=load_pdf_file(data='data/')
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks=text_split(filter_data)

embeddings = download_embeddings()

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)



index_name = "medical-chatbot" 

if pc.has_index(index_name):
    pc.delete_index(index_name)

pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

index = pc.Index(index_name)


# Initialize vector store
docsearch = PineconeVectorStore(
    index_name=index_name,
    embedding=embeddings,
    pinecone_api_key=PINECONE_API_KEY  
)

# Function to divide into batches
def batch_iterate(size, iterable):
    """Yields batches of the given size from the iterable."""
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]

# Add documents in batches of 50 to avoid hitting the 4MB limit
print(f"Uploading {len(text_chunks)} chunks in batches...")
for i, batch in enumerate(batch_iterate(50, text_chunks)):
    print(f"Processing batch {i+1}...")
    docsearch.add_documents(batch)

print("Ingestion complete.")