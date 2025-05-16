#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Utilities for both OpenAI API and local AITA modules. These include 3 functions and two sub-functions:
#1. generate_prompt: creating the prompt
#2. extract_response: extracting the JSON and summary blocks,
#3. output_aita: inserting the JSON from AITA to the CSV, if writing report selected printing the summary to a file.
#4. subfunctoins is_valid_json and fix_json - two sub-functoins of output aita, for the purpose of fixing responses with invalid json strings.

import sys
import os
import pandas as pd
from datetime import datetime
import json
import re

try:
    base_path = os.path.dirname(__file__)              # getting the file paths when running in CLI 
except NameError:
    base_path = os.getcwd()                            # getting the file paths when running in Jupyter Notebooks
sys.path.append(os.path.join(base_path, 'parser'))
sys.path.append(os.path.join(base_path, 'AITA'))

project_root = os.path.abspath(os.path.join(base_path, ".."))
sys.path.append(project_root)

# Creating the prompt for the LLM. Takes a base prompt from text file and appends the parsed log.

def generate_prompt(parsed_log_path, write_report=False):                  

    with open(parsed_log_path) as parsed_file:
        log_content = parsed_file.read()

    prompt_path = os.path.abspath(os.path.join(base_path, "..", "AITA", "baseprompt.txt"))

    with open(parsed_log_path) as parsed_file:
        log_content = parsed_file.read()

    with open(prompt_path, "r") as promptfile:
        base_prompt = promptfile.read()

    prompt = base_prompt+log_content
      
    if write_report:
        prompt += '''
        After the JSON block, write the line ---COMMENCE-REPORT---, and then write a brief report (maximum 50 words) summarizing the findings in natural language.
        This report must appear on a new line after the JSON and must not be inside the JSON itself.
        '''

    return prompt

# Extracting the log lines and the AITA report if report is selected. 
def extract_response(LLM_output):                              
    partitioned = LLM_output.partition("---COMMENCE-REPORT---")
    row_list = partitioned[0]
    if "json" in row_list:
        row_list = row_list.replace("```json", "")
        row_list = row_list.replace("```", "")
    return row_list.strip(), partitioned[2].strip()

# Subfunction checking if string is valid json.
def is_valid_json(tested_string):
    try:
        data = json.loads(tested_string)
        valid = True
    except json.JSONDecodeError:
        valid = False
    return valid

# Subfunction to fix the string if it is not valid json.
def fix_json(string_to_fix):
    string_to_fix = string_to_fix.partition("---COMMENCE-REPORT---")[0]
    start = string_to_fix.find('[')
    end = string_to_fix.rfind(']')
    if start != -1 and end != -1 and end > start: string_to_fix=string_to_fix[start:end+1]
    string_to_fix.split(']', 1)[0] + ']'
    string_to_fix = string_to_fix.strip()
    string_to_fix = re.split(r"-{2,}\s*COMMENCE-REPORT\s*-{2,}", string_to_fix, flags=re.IGNORECASE)[0]

    if not string_to_fix.startswith("["): string_to_fix = "["+string_to_fix
    if not string_to_fix.endswith("]"): string_to_fix = string_to_fix+"]"
    
    string_to_fix = string_to_fix.replace("{{", "{").replace("}}", "}")        
    string_to_fix = string_to_fix.replace("[[", "[").replace("]]", "]")
    string_to_fix = re.sub(r",\s*]", "]", string_to_fix)
    string_to_fix = re.sub(r",\s*}", "}", string_to_fix)
    string_to_fix = re.sub(r'(?<!["\'])\b(\w+)\b(?=\s*:)', r'"\1"', string_to_fix)
    string_to_fix = re.sub(r'^\[\s*"row":', r'[{"row":', string_to_fix)
    string_to_fix = re.sub(r'\}\s*\]$', r'}]', string_to_fix)  # just in case it ends weirdly
        
    string_to_fix = string_to_fix.replace("```json", "")
    string_to_fix = string_to_fix.replace("```", "")
    string_to_fix = string_to_fix.replace("''", "'")
    string_to_fix = string_to_fix.replace('""', '"')
    
    return string_to_fix

# Outputing the AITA response to CSV and to a report text file if report is selected.
def output_AITA(filepath, extracted_response, model="None", time=0, print_mode=False):   
    aita_list = extracted_response[0]
    if not is_valid_json(aita_list):
        aita_list = fix_json(aita_list)
    aita_list = json.loads(aita_list)
    
    for item in aita_list:
        item["risk_level"] = int(item["risk_level"])
    aita_combined = pd.read_csv(filepath)              # creating a dataframe.
    aita_combined["aita_risk_level"] = 1               # dataframe filled with default 1 risk level, no comment.
    aita_combined["aita_comment"] = ""

    for line in aita_list:
        row_number = line["row"]
        aita_combined.loc[row_number, "aita_risk_level"] = line["risk_level"]
        aita_combined.loc[row_number, "aita_comment"] = line["comment"]
    
    aita_combined.to_csv(filepath, index=False)        # writing the combined dataframe to csv file.

    ### The following segment is in case report mode is selected.
    
    if extracted_response[1] != "":                    # preparing the report text.
        report_datetime = str(datetime.now())
        report_date, milisecs = report_datetime.rsplit(".", 1)
        lines_list = ", ".join(str(line["row"]) for line in aita_list)
        report = f"""AI TRIAGE ASSISTANT SUMMARY REPORT:
-----------------------------------
Report date: {report_date}
Analyzed log file: {filepath} | Model: {model} | Time to process: {time:.4f} seconds
Number of suspected lines (risk level above 1): {len(aita_list)}
Suspected lines: {lines_list}

AITA SUMMARY:
-------------
{extracted_response[1]}
"""
        if print_mode: print(report)
        
        filename_base, ext = filepath.rsplit(".", 1)               # Set filename as parsed_log_path-AITA_report.txt, and write report to it.
        filename = filename_base + "-AITA_report.txt"
        with open(filename, "w") as reportfile:        
            reportfile.write(report)

