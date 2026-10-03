import os
from typing import TypedDict

#Creation of the state

class pipelinestate(TypedDict):
    raw_data: str
    edited_text: str
    script_text: str
    final_output: str
    
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0.7, api_key=os.getenv("GROQ_API_KEY"))

def editor_node(state: pipelinestate) -> dict:
    '''Stage 1: Cleans up grammar, removes typos, and improves the tone.'''
    prompt = f"Please edit the following text for grammar, typos, and tone:\n\n{state['raw_data']}"
    response = llm.invoke(prompt)
    return {"edited_text": response.content.strip()}


def scriptwriter_node(state: pipelinestate) -> dict:
    '''Stage 2: Converts the edited text into a short-form video script.'''
    prompt = f"Convert the following edited text into an engaging short-form video script:\n\n{state['edited_text']}"
    response = llm.invoke(prompt)
    return {"script_text": response.content.strip()}


def final_output_node(state: pipelinestate) -> dict:
    '''Stage 3: Converts the script into Hinglish.'''
    prompt = f"Convert the following script into natural Hinglish. Keep the meaning and structure the same. Return only the Hinglish script:\n\n{state['script_text']}"
    response = llm.invoke(prompt)
    return {"final_output": response.content.strip()}

#Using Langraph
from langgraph.graph import StateGraph , START, END

graph = StateGraph(pipelinestate)

#Adding nodes to the graph
graph.add_node("editor", editor_node)
graph.add_node("scriptwriter", scriptwriter_node)
graph.add_node("final_output", final_output_node)


#Sequential (Addition of Edges)

graph.add_edge(START, "editor")
graph.add_edge("editor", "scriptwriter")
graph.add_edge("scriptwriter", "final_output")
graph.add_edge("final_output", END)

#compile the graph
app = graph.compile()
inpui = input("Enter the text to be processed: ")
result = app.invoke({"raw_data": inpui})
print(result['final_output'])