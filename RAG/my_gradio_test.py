import gradio as gr
import requests
from FlagEmbedding import FlagReranker
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import openai
import os
from langchain_community.document_loaders import (PyPDFLoader, 
                                        JSONLoader,
                                        UnstructuredMarkdownLoader,
                                        TextLoader)
from langchain.prompts import PromptTemplate
from langchain import LLMChain
# from langchain_openai import OpenAIEmbeddings


URL = "http://127.0.0.1:9898"
bge_path = "/Users/zyl/Desktop/LLM/pretrain_models/bge-base-zh-v1.5"
reranker_path = "/Users/zyl/Desktop/LLM/pretrain_models/bge-reranker-base/"
os.environ["OPENAI_API_KEY"] = "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"
# openai_embeddings = OpenAIEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name=bge_path)
reranker = FlagReranker(reranker_path, use_fp16=True)


def llm_request_api(message, history):
    data = {
        "prompt": message,
        "history": [],
        "max_length": 4096,
        "top_p": 0.8,
        "temperature": 0.7
    }
    response = requests.post(URL, json=data)
    catbot= response.json()["response"]
    return catbot


def split_file_and_parser(file_path):
    if file_path is not None:
        if file_path.name.endswith('txt'):
            txt_loader = TextLoader(file_path.name)
            loader = txt_loader.load()
        elif file_path.name.endswith('pdf'):
            pdf_loader = PyPDFLoader(file_path.name)
            loader = pdf_loader.load()
        elif file_path.name.endswith('docx'):
            from docx import Document
            pass
    text_splitter = CharacterTextSplitter(separator="\n", 
                                            chunk_size=200, 
                                            chunk_overlap=0, 
                                            length_function=len)
    docs = text_splitter.split_documents(loader)
    db = FAISS.from_documents(docs, embeddings)
    # query = "What is this document mainly about？"
    print("完成了Faiss数据库的解析工作。------------------------------------")
    return db


def struc_content(db, query):
    docs_and_scores = db.similarity_search_with_score(query, k=5)
    contents = [d[0] for d in docs_and_scores]
    query_content_list = [[query, content.page_content] for content in contents]
    scores = reranker.compute_score(query_content_list)
    topk_ = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:2]
    select_texts = "" 
    for i, (ind, _) in enumerate(topk_):
        select_texts += "-----------Rank_{}---------\n".format(i+1)
        select_texts += contents[ind].page_content
        select_texts += "\n"
    return select_texts


def gpt_model(db, query):
    from langchain.llms import OpenAI
    GPT = OpenAI(model_name='gpt-3.5-turbo')
    content = struc_content(db, query)
    prompt_template = """您是一位文档分析专家，请您仅依据下列Content中的内容，回答Question中的问题。
    Content: {Input}
    Question: {question}
    No more than 20 characters in Chinese:
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["Input", "question"])
    llm_chain = LLMChain(prompt=PROMPT, llm=GPT)
    result = llm_chain.run(Input=content, question=query)
    return result, content


def glm_model(db, query):
    content = struc_content(db, query)
    prompt_template = """您是一位文档分析专家，请您仅依据下列Content中的内容，回答Question中的问题。
    Content: {}
    Question: {}，和证券运维行业相关的是有效文档，请输出"有效文档", 其他都是无效文档，请输出"无效文档"。
    Answer in Chinese:
    """.format(content, query)
    result = llm_request_api(prompt_template, history=[])
    return result, content


def process_file(db, S, query):
    if S == "GLM":
        result, out_content = glm_model(db, query)
    elif S == "GPT":
        result, out_content = gpt_model(db, query)
    print(out_content)
    return result, out_content


with gr.Blocks() as demo:
    gr.HTML("""<h1>对话和文档解析</h1>""")
    with gr.Tab("对话"):
        demo2 = gr.ChatInterface(llm_request_api)
    with gr.Tab("文档解析"):
        # 上传文档
        update_file = gr.File(label="上传文件")  
        
        # 解析文档到Faiss
        submit_btn = gr.Button("文档解析")
        data_db = gr.State()
        submit_btn.click(fn=split_file_and_parser, inputs=[update_file], outputs=[data_db])

        # 问答过程
        with gr.Row():
            with gr.Column(scale=1):
                S = gr.Radio(["GPT", "GLM"], label="GPT or GLM", value="GLM")
            with gr.Column(scale=4):
                query = gr.Textbox(value="学费多少钱？", label='Query')
        # 解析文档到Faiss
        anwser_btn = gr.Button("问答")
        # result_output = gr.State()
        with gr.Tab('output'):
            result_output = gr.Textbox(label="分析结果")
        with gr.Tab('content'):
            out_content = gr.Textbox(label="Topk嵌入数据", lines=7)
        anwser_btn.click(fn=process_file, inputs=[data_db, S, query], outputs=[result_output, out_content])



if __name__ == "__main__":
    
    demo.launch(share=True)
