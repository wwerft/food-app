from dotenv import load_dotenv

from typing import Any, Dict, List

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore


# Umgebungsvariablen laden
load_dotenv()

# Pinecone-Index definieren
INDEX_NAME = "ernaehrungsberater-doc-index"

# Korrigierte Prompt-Vorlage mit den richtigen Variablen
retrieval_qa_chat_prompt = PromptTemplate(
    input_variables=["context", "input"],
    template=(
        "Du bist ein Ernährungsberater für Profisportler. Nutze den folgenden Kontext, "
        "um die Frage bestmöglich zu beantworten. Ergänze mit Hilfe des Wissens aus dem Netz."
        "Antworte wissenschaftlich und erkläre die Wirkungen der Stoffe."
        "Gehe von fehlenden Fachkenntnissen aus und erkläre Wirkstoffe und Prozess im Körper einfach und bildlich."
        "Ergänze Mengenangaben zur Einnahme, sofern diese sinnvoll sind. Strukturiere die Antwort übersichtlich  :\n\n"
        "Kontext:\n{context}\n\n"
        "Frage: {input}\n\n"
        "Antwort:"
    ),
)


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
#     rephrase_prompt = PromptTemplate(
#         input_variables=["chat_history", "input"],
#         template=(
#             "Given the following conversation and a follow up question, rephrase the follow up"
#             "question to be a standalone question.\n\n"
#             "Chat History:"
#             "{chat_history}"
#             "Follow Up Input: {input}"
#             "Standalone Question:"
#         ),
#     )

    # retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
    )
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"],
    }
    return new_result


if __name__ == "__main__":
    query = "Welche Dinge haben eine positive Wirkung auf Sportler?"
    print(f"Frage an das Modell: {query}")
    res = run_llm(query=query)
    print(res["result"])
