#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### This is the LoPTA command-line tool and main script.

import sys
import os
try:
    base_path = os.path.dirname(__file__)              # getting the file paths when running in CLI 
except NameError:
    base_path = os.getcwd()                            # getting the file paths when running in Jupyter Notebooks
sys.path.append(os.path.join(base_path, 'parser'))
sys.path.append(os.path.join(base_path, 'AITA'))

import argparse
from parser.log_parser import parse_log
from AITA import AITA_chat
from AITA import AITA_local
from AITA import AITA_utils
import time


signature = r"""
Usage example:
python lopta.py .\sample_logs\auth.log -o .\output\auth_parsed.csv -c -r -p 
^--- parse .\sample_logs\auth.log, output to .\output\auth_parsed.csv, with AITA analysis (ChatGPT, default model GPT-4o-mini) and report,
and with on-screen printing.   

~       (\__/)
~      ( •ㅅ•)
~     (⤙    )⤙
~  .__/ .__/ CYB3R J3RB04
~        leap • evade • adapt
    
"""

## Parser definitions
cl_parser = argparse.ArgumentParser(
    description="*** LoPTA - Log Parser and Triage Assistant ***",
    epilog=signature,
    formatter_class=argparse.RawDescriptionHelpFormatter
)

cl_parser.add_argument("FILENAME", help="Name of log file to parse.")
cl_parser.add_argument("-t", "--type", help="Type of log file. Options: auth, access, error. If not set, LoPTA will infer from filename.")
cl_parser.add_argument("-o", "--output", help="Name of output CSV file. If not set, LoPTA will run in print only mode.")
cl_parser.add_argument("-p", "--print", action="store_true", help="Print mode. LoPTA will print the log parser output on screen.")
cl_parser.add_argument("-l", "--ollama", nargs="?", const="mistral", help="""AI Triage Assistant, local mode using Ollama. State LLM model.
If none given, default is Mistral. Note: Ollama must be running. AITA requires --output to be set.""")
cl_parser.add_argument("-c", "--chat", nargs="?", const="gpt-4o-mini", help="""AI Triage Assistant, OpenAI API mode. State OpenAI model.
If none given, default is GPT-4o-mini. NOTE: OpenAI API key required!!!
API Key can be: 1. saved in ./AITA/openai_key.txt; 2. saved as environment variable OPENAI_API_KEY; 3. input manually when running.
AITA requires --output to be set.""")
cl_parser.add_argument("-r", "--report", action="store_true", help="""Attach AITA summary report. In output mode, 
it will be saved in the same name as the CSV file, ending with -AITA-report.txt. In print mode, it will appear after the parsed log.""")
cl_parser.add_argument("-v", "--version", action="version", version='LoPTA 1.0')


args = cl_parser.parse_args()

## AITA logic breaks.
if (args.chat is not None or args.ollama is not None) and not args.output:
    sys.exit("AITA requires output to be set.")
elif args.chat and args.ollama:
    sys.exit("Alas, you must choose EITHER Chat-GPT AITA OR local Ollama AITA.")

## Determine log type if not set.
if not args.type:
    if "auth" in args.FILENAME:
        args.type = "auth"
        print("Log file type set to auth.")
    elif "access" in args.FILENAME:
        args.type = "access"
        print("Log file type set to access.")
    elif "error" in args.FILENAME:
        args.type = "error"
        print("Log file type set to error.")
    else:
        sys.exit("Log type not provided and could not be inferred from filename.")

if not args.output:
    print("Output path not set. Printing to screen only.")
    args.print = True


parse_log(args.FILENAME, args.type, args.output, args.print)
print("LOG PARSING COMPLETE.")

# AITA module logic, whether chat or local.
if args.chat:
    print("Running AITA. Please be patient...")
    start_time = time.time()
    AITA_response = AITA_chat.aichat(args.output, args.chat, write_report=args.report)
    end_time = time.time()
    processing_time = end_time - start_time
    extracted = AITA_utils.extract_response(AITA_response)
    AITA_utils.output_AITA(args.output, extracted, args.chat, time=processing_time, print_mode=True)
    print("AITA OPERATION COMPLETED SUCCESSFULLY.")
if args.ollama:
    print("Running AITA. Please be patient...")
    start_time = time.time()
    AITA_response = AITA_local.AIlocal(args.output, args.ollama, write_report=args.report) ###CHANGE AILOCAL FUNC NAME
    end_time = time.time()
    processing_time = end_time - start_time
    extracted = AITA_utils.extract_response(AITA_response)
    AITA_utils.output_AITA(args.output, extracted, args.ollama, processing_time, print_mode=args.print)
    print("AITA OPERATION COMPLETED SUCCESSFULLY.")

