#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os
sys.path.append(os.path.abspath(".."))
from openai import OpenAI
from AITA import AITA_utils

try:
    base_path = os.path.dirname(__file__)              # getting the file paths when running in CLI 
except NameError:
    base_path = os.getcwd()                            # getting the file paths when running in Jupyter Notebooks

aita_key_path = os.path.join(base_path, "openai_key.txt")

def aichat(parsed_log_path, gptmodel, write_report=False):
     
    # Get the API Key, in order: 1. environmental, 2. file, 3. input

    if "OPENAI_API_KEY" in os.environ:
        openai_key = os.environ["OPENAI_API_KEY"]
    elif os.path.exists(aita_key_path):
        with open(aita_key_path) as openai_key_file:
            openai_key = openai_key_file.read()
    else:
        openai_key=input("Enter OpenAI API Key: ")
    
    client = OpenAI(api_key=openai_key)

    prompt = AITA_utils.generate_prompt(parsed_log_path, write_report)
    
    # Create a completion
    completion = client.chat.completions.create(
        model=gptmodel,
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    output_text = completion.choices[0].message.content
    
    return output_text

