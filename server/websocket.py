import asyncio
import websockets
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langgraph.graph import END, MessageGraph
import os
import git
import re
import json

def filter_important_files(file_paths):
    important_extensions = [
    '.php'
]

    important_files = []
    for file_path in file_paths:
        if any(file_path.endswith(ext) for ext in important_extensions):
            important_files.append(file_path)
    
    return important_files


def clone_repo(repo_url, clone_dir):
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    repo = git.Repo.clone_from(repo_url, clone_dir)
    return repo.working_tree_dir



def list_files(directory):
    file_list=[]
    for root, dirs, files, in os.walk(directory):
        for file in files:
            if "." in file[0]:
                continue
            else:
                file_list.append(os.path.relpath(os.path.join(root,file,), directory))
    return file_list




def read_file(file_path):
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File not found.")
        return None
    
summarizer = """ 

Task: Analyzing GitHub Repository Files for Web Vulnerabilities

Description: Your task is to meticulously analyze GitHub repository files for potential web vulnerabilities that could compromise security. Specifically, focus on identifying vulnerabilities such as SQL injection (SQLi), cross-site scripting (XSS), and other common web attack vectors. Pinpoint any code segments or patterns that pose a risk to software security.

Output Format:
For each identified web vulnerability, provide the following details:

Vulnerability Type: Specify the type of vulnerability found (e.g., SQL injection, XSS).
Location: Full file path and line numbers where the vulnerability is present.
Line Number: Only include the line numbers where the vulnerability exists.
Solution: Provide a solution to mitigate the vulnerability. Ensuring to include the full solution.
Ensure thorough analysis to accurately identify and address potential web vulnerabilities, fortifying the GitHub repository against security threats.

Output Formate only json for text and markup for code:


the code should be in markup format
Just stick to formate no extra text here is the code or I find this or that

{
    "vulnerability_type":"vulnerability_type",
    "any_vulnerability_found":"true/false",
    "location":"full_file_path",
    "line_number":"line_number",
    "vulnerability_description":"vulnerability_description",
    "solution_description":"solution_description"
}

"""

def llm():
    instruction = """
    You are provided with a file content and a description of what vulnerability is present in that file and approximation of which near which line, your task is to reply to the user about the same vulnerabilty. No other vulnerabilty is allowed.
    Don't talk about anything else

"""
    




directory = os.path.abspath(os.getcwd()) 
file_name = "summary.txt"
model = Ollama(model="mistral", 
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
             verbose=False,
             temperature=0)

graph = MessageGraph()
graph.add_node("oracle", model)
graph.add_edge("oracle", END)
graph.set_entry_point("oracle")
runnable = graph.compile()




async def echo(websocket, path):
    async for message in websocket:
        json_message = json.loads(message)
        if(json_message["url"]):
            
            print(json_message["url"])
            github_url = json_message["url"]
            match = re.search(r"\/([^\/]+)\/?$", github_url)
            clone_file_name = match.group(1).replace(".git","")
            repo_path = clone_repo(github_url, clone_file_name)
            files = list_files(repo_path)

            file_list = filter_important_files(files)

            file_structure = {"file_structure": files}
            await websocket.send(json.dumps(file_structure))

            send_length = {"file_length": len(file_list)}

            print(json.dumps(send_length))

            await websocket.send(json.dumps(send_length))
            
            if(len(file_list) == 0):
                send_error_json = {"error": "The provided GitHub Repo doesn't contain any .php file."}
                await websocket.send(json.dumps(send_error_json))
                break

            
            for files in file_list:
                
                file_path = os.path.abspath(os.getcwd())+"/"+clone_file_name+"/"+files
                print(file_path)
                file_content = read_file(file_path)
                finalize = (file_content + f"file_name:{files} " + summarizer)
                result = runnable.invoke(finalize)
                string_message = str(result[1].content)
                output_message = f"""{string_message}"""

                output_directory = directory+"/"+clone_file_name+"_analysis"
                match = re.search(r"/([^/]+)$", files)

                if match:
                    last_part = match.group(1)
                    last_part = last_part+".txt"
                    print(last_part)  # Output: secondorder_changepass.php
                else:
                    print("No match found")

                await websocket.send(str(output_message))
                print("Sent to client")
            if(json_message["llm"]):
                print("not")

            send_status_completed =   {"status": "completed"}  
            await websocket.send(json.dumps(send_status_completed))
        
        
        
        
        
        
       







async def main():
    # Start the WebSocket server
    async with websockets.serve(echo, "localhost", 8765):
        print("WebSocket server started...")
        
        # Keep the server running
        await asyncio.Future()  # Run forever

asyncio.run(main())
