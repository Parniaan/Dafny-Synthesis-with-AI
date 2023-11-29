import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader

load_dotenv()
pdf_folder_path = ''
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Document loaders
# link: https://python.langchain.com/docs/modules/data_connection/document_loaders/
def load_data_from_txt(file_path):
  loader = TextLoader(file_path)
  data = loader.load()
  raw_text = ''
  for document in data:
    page_content = document.page_content
    if page_content:
      raw_text += page_content

  return raw_text

def load_data_from_pdf(file_path):
  loader = PyPDFLoader(file_path)
  pages = loader.load_and_split()
  return pages;

# Split the text that into smaller chuncks so that during information retrival 
# we don't hit the token size limits.
def split(raw_text):
  text_splitter = RecursiveCharacterTextSplitter(
    separators = [".",],
    chunk_size = 1000,
    chunk_overlap = 200,
    # length_function = len,
  )
  texts = text_splitter.split_text(raw_text)
  return texts;


def main():
    while True: 
        file_path = input("Enter path to PDF file for indexing: ")
        file_path = file_path.strip()
        # Extract the file name from the input_file_path without the extension
        input_file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        if file_extension != '.pdf':
            print('Error: PDF document is required!')
        else:
            out_file = f'{input_file_name}_index'

            # download embeddings from OpenAI
            embeddings = OpenAIEmbeddings()

            pages = load_data_from_pdf(file_path)
            db = FAISS.from_documents(pages, embeddings)
            db.save_local("faiss_index", out_file)
            print('- - - - embedding is done - - - -')

if __name__ == "__main__":
    main()

