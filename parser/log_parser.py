#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## This is the main core parser of LoPTA. It loads patterns from patterns.py.
import sys
import os
sys.path.append(os.path.abspath(".."))

import re
import pandas as pd
from parser.patterns import *

def parse_log(input_path, log_file_type, output_path=None, print_mode=False):

    pattern_map = {
    "auth": auth_patterns,
    "access": access_patterns,
    "error": error_patterns
}

    patterns = pattern_map.get(log_file_type)
    
    with open(input_path) as auth_log:
        log_lines = auth_log.readlines()

    if log_lines == []:
        sys.exit("ERROR: Empty log file.")
    
    
    parsed_logs = []

# Insert attribute log_type, by pattern matched, fallback to unknown pattern if no match.
    for log_line in log_lines:
        matched = False
        for log_type, pattern in patterns.items():
            match = pattern.search(log_line)
            if match:
                entry = match.groupdict()
                entry["log_type"] = log_type                                  
                parsed_logs.append(entry)
                matched = True
                break  # stop after first match
        if not matched:
                match = unknown_pattern.search(log_line)
                entry = match.groupdict()
                entry["log_type"] = "unknown pattern"
                parsed_logs.append(entry)
                matched = True
    
# Output to CSV if output option selected.
    if output_path != None: 
        parsed_logs_pd = pd.DataFrame(parsed_logs)
        parsed_logs_pd.to_csv(output_path, index=False)

# Print to screen if print mode selected.
    if print_mode == True:
        if log_file_type == "auth":
            for num, entry in enumerate(parsed_logs, start=1):
                print(f"""
                LOG NO. {num} ({entry['log_type']}):\tTime: {entry.get('timestamp')} | 
                Host: {entry.get('host')} | Service: {entry.get('service')} | Status: {entry.get('raw_status')}
                User: {entry.get('user')} | IP Address: {entry.get('ip_address')} |
                Calling User: {entry.get('calling_user')} | Target User: {entry.get('target_user')} | Command: {entry.get('command')}
                """)
                if entry.get('err_message'): print (f"UNKNOWN LOG TYPE. MESSAGE: {entry.get('err_message')}") 

        elif log_file_type == "access":
            for num, entry in enumerate(parsed_logs, start=1):
                print(f"""
                LOG NO. {num} ({entry['log_type']}):\tTime: {entry.get('timestamp')} | 
                IP address: {entry.get('ip_address')} | Method: {entry.get('method')} | Path: {entry.get('path')}
                | Protocol: {entry.get('protocol')} | Status Code: {entry.get('status_code')} | Response Size: {entry.get('response_size')}
                | Referrer: {entry.get('referrer')} | User Agent: {entry.get('user_agent')} 
                """)
                if entry.get('err_message'): print (f"UNKNOWN LOG TYPE. MESSAGE: {entry.get('err_message')}") 

        elif log_file_type == "error":
            for num, entry in enumerate(parsed_logs, start=1):
                print(f"""
                LOG NO. {num} ({entry['log_type']}):\tTime: {entry.get('timestamp')} | 
                Module: {entry.get('module')} | Level: {entry.get('level')} | PID: {entry.get('pid')} | TID: {entry.get('tid')}
                | Client IP Address: {entry.get('client_ip')} | Client Port: {entry.get('client_port')} | Error Code: {entry.get('error_code')}
                | Message: {entry.get('message')} 
                """)
                if entry.get('err_message'): print (f"UNKNOWN LOG TYPE. MESSAGE: {entry.get('err_message')}") 

