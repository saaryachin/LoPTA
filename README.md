# LoPTA - Log Parser and Triage Assistant

## About

LoPTA assists in parsing Linux logs and triaging security information. It comprises two modules:
* **Parser** - Lopta parses logs into a .csv file. Each log line is made into a row, with separate columns for the important data. The columns change according to log type. LoPTA 1.0 supports auth.log and Apache2 access.log and error.log formats.
* **AITA** - The AI Triage Assistant adds two more columns to the parser's output CSV - risk level as assigned by the LLM, and a comment for notable rows. **AITA** has two modes - Chat-GPT models based on OpenAI's API, and local on the basis of Ollama.

## What it does

Given a log file, LoPTA either outputs it to a csv file, or prints it on screen. If AITA is activated, LoPTA will add columns from the AI Triage Assistant, and can also include a summary report in a separate file.

## Requirements

* Python 3.9+
* Dependencies:
 * pandas
 * openai
 * requests

To install all dependencies:
```bash
pip install -r requirements.txt
```
## Run it

Lopta is run from CLI. 

```bash
usage: python lopta.py [-h] [-t TYPE] [-o OUTPUT] [-p] [-l [OLLAMA]] [-c [CHAT]] [-r] [-v] FILENAME
```

For more information, simply run:
```bash
python lopta.py --help
```
## Files in this repository

I also included the .ipynb Jupyter notebooks for reference, but omitted them from the following tree.

```bash
LoPTA/
├── lopta.py                        # The main command line script. 
├── parser/                           # The parser module
│   ├── `__init__`.py
│   ├── log_parser.py
│   └── patterns.py                 # Regex patterns for auth.log, access.log, error.log
│
├── AITA/                               # The AI Triage Assistant module.
│   ├── `__init__`.py
│   ├── AITA_chat.py
│   ├── AITA_local.py
│   ├── baseprompt.txt             # The base prompt used for AITA.
│   ├── openai_key.txt              # Not included :) but if you have an API key it goes here.
│   └── AITA_util.py                    # Common functions used by the local and OpenAI AITA options. 
│
├── sample_logs/                     # Sample logs for testing
│   ├── auth.log
│   ├── access.log
│   ├── error.log
│   └── malformedauth.log                 # Malformed auth.log to test handling of malformed lines.
│
├── outputs/                                        # Two example output files for demonstration.
│   ├── authlog_chatgpt.csv                          # example of AITA with OpenAI API.
│   ├── authlog_chatgpt-AITA-report.csv      # AITA report for above file.
│   ├── accesslog_mistral.csv                         # example of AITA with Mistral through Ollama.
│   └── accesslog_mistral-AITA-report.csv    # AITA report for above file.
│
├── requirements.txt                     # Python dependencies
├── README.md                            # You are here :)
├── Learning Journal - LoPTA Project.md  # My study notes, for myself and for you should you like.
└── LICENSE
```

## Discussion of the AITA model

### Example of an AITA Report:

```bash
AI TRIAGE ASSISTANT SUMMARY REPORT:
-----------------------------------
Report date: 2025-05-16 10:18:29
Analyzed log file: .\output\authlog_chatgpt.csv | Model: gpt-4o-mini | Time to process: 4.2080 seconds
Number of suspected lines (risk level above 1): 6
Suspected lines: 3, 5, 7, 13, 15, 20

AITA SUMMARY:
-------------
Multiple failed password attempts and an invalid user login indicate potential unauthorized access attempts. Monitoring and further investigation are recommended to mitigate risks.
```
### AITA-chat (OpenAI API)

#### Requirements: 

AITA works most efficiently through the OpenAI API. The default model is ChatGPT-4o-mini, which is very cost effective and did a very decent job in my trials. Having run around 2,000 log lines, it set me back only a few cents, with perfect results. However, naturally it is not best practice to process your security logs in the cloud. Therefore AITA also has a local mode.
#### AITA-local (Ollama)

The local mode is based on Ollama. I have tried 3 LLMs that can work reasonably well on my modest machine: Phi-3, which was relatively fast and pretty decent; Mistral, which gave better results but took longer, and Tinyllama, which was fast with garbled hallucinations rendering it useless. Much of the work has gone into cleaning up the responses received from the models running on Ollama. I can only hope that the functions for clearing up the responses will cover most of their misses.

The ideal setup would be a stronger model with RAG, running on a more capable machine (RAM and GPU). That would eliminate the need for the OpenAI API for smoother flow.

### Should there ever be LoPTA ver. 2.0...

- I would consider using llama.cpp instead of Ollama, for better performance and because I don't like the persistent Ollama daemon.
- Ideally, AITA would be run locally, with a more capable model and RAG. Perhaps LoPTA 2.0 could enable tethering to a dedicated workstation for running an LLM.
- The parser model would be expanded to recognize and parse more log types and patterns.
- Error handling would be improved (unknown models, malformed logs, etc.).

## Additional materials

If you are interested, you can have a look at my [Learning Journal](Learning%20Journal%20-%20LoPTA%20Project.md).

## License

This project is licensed under the [MIT License](LICENSE).
