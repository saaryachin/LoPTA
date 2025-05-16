#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os
sys.path.append(os.path.abspath(".."))
import requests
from AITA import AITA_utils

def AIlocal(parsed_log_path, model, write_report=False):

    try:
        base_path = os.path.dirname(__file__)              # getting the file paths when running in CLI 
    except NameError:
        base_path = os.getcwd()                            # getting the file paths when running in Jupyter Notebooks
        
        sys.path.append(os.path.join(base_path, 'parser'))
        sys.path.append(os.path.join(base_path, 'AITA'))
    prompt = AITA_utils.generate_prompt(parsed_log_path, write_report)
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
            "temperature": 0.3
            }
        }
    )
    AITA_output = response.json()["response"]
    return AITA_output


