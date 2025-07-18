import base64
import requests
import json
import sys
import re

ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:12b"
isQwen = False

def query_model(prompt=""):
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "incremental_output": True
    }

    if MODEL_NAME == "qwen3:14b":
        global isQwen 
        isQwen = True
    
    headers = {
        "X-DashScope-SSE": "enable", 
        "Content-Type": "application/json"
    }

    full_response = ""

    try:
        with requests.post(ENDPOINT, json=payload, headers=headers, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8").strip()
                    try:
                        data = json.loads(decoded)
                        chunk = data.get("response", "")
                        print(chunk, end="", flush=True)    
                        full_response += chunk               
                    except json.JSONDecodeError:
                        print(f"[Invalid JSON] {decoded}", flush=True)

        return full_response
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def translate(file, SRC, TGT):
    
    cout = 1
    lines = []
    global isQwen
    global TRANSLATIONS

    for line in file:

        lines.append(line)
        cout+=1

        if cout == 6:
            response = query_model(f"""You are a translator for {SRC} to {TGT}. Please provide the translation for the following sentences using the format below. Don’t provide additional text or explanation.

Sentences:

1. {lines[0]}
2. {lines[1]}
3. {lines[2]}
4. {lines[3]}
5. {lines[4]}

Format:

SRC: [source_text]
TGT:""")
           
            wothinkres = response

            if isQwen:
                wothinkres = re.sub(r"<think>.*?</think>\s*", "", response, flags=re.DOTALL) 

            TRANSLATIONS.write(f"{wothinkres}\n\n")
            lines.clear()
            cout = 1

    file.close()
        
        
        
FILE_PATH = r"translated.txt"
TRANSLATIONS =  open("translations.txt", "w", encoding="utf-8")
SRC = "ENGLISH"

LANG  = ["CEBUANO", "ILOCANO", "TAGALOG"]

if SRC in LANG:
    LANG.remove[SRC]

for TGT in LANG:
    print(TGT)

    FILE = open(FILE_PATH, 'r', encoding="utf-8")
    translate(FILE, SRC, TGT)