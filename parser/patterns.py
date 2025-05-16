#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## This file contains the regex patterns for the different log types.

import re

__all__ = [
    "auth_patterns",
    "access_patterns",
    "error_patterns",
    "unknown_pattern"
]


#########################
# PATTERNS FOR auth.log #
#########################

auth_patterns = {                                                   
    "ssh_login": re.compile(r'''                                    #ssh_login line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>\w+(?:\[\d*\])?):
    \s+(?P<raw_status>(Accepted|Failed)\s+(?:password|publickey))\s+for\s+(?P<user>\S+)\s+from\s+(?P<ip_address>\d{1,3}(?:[-.]\d{1,3}){3}) 
    ''', re.VERBOSE),

    "sudo": re.compile(r'''                                         #sudo line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>sudo):
    \s+(?P<calling_user>\w+)\s+:
    .*?
    USER=(?P<target_user>\w+)
    .*?
    COMMAND=(?P<command>.+)
    ''', re.VERBOSE),

    "pam_session": re.compile(r'''                                  #pam_session line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>\w+(?:\[\d*\])?):\s+pam_unix
    .*?
    (?P<raw_status>session\s+(?:opened|closed))
    \s+for\s+user\s+(?P<user>\S+)
    ''', re.VERBOSE),

     "invalid_user_failed_pw": re.compile(r'''                       #invalid_user_failed_pw line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>\w+(?:\[\d*\])?):
    \s+(?P<raw_status>Failed\s+password)\s+for\s+invalid\s+user\s+(?P<user>\S+)\s+from\s+(?P<ip_address>\d{1,3}(?:\.\d{1,3}){3}) 
    ''', re.VERBOSE),

    "invalid_user_proper": re.compile(r'''                            #invalid_user_proper line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>\w+(?:\[\d*\])?):
    \s+(?P<raw_status>Invalid\s+user)\s+(?P<user>\S+)\s+from\s+(?P<ip_address>\d{1,3}(?:\.\d{1,3}){3}) 
    ''', re.VERBOSE),

    "invalid_user_userauth": re.compile(r'''                                            #invalid_user_userauth line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>\w+(?:\[\d*\])?):
    \s+input_userauth_request:\s+(?P<raw_status>invalid\s+user)\s+(?P<user>\S+) 
    ''', re.VERBOSE),
    
    "connection_closed": re.compile(r'''                                    #connection_closed line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>\w+(?:\[\d*\])?):
    \s+(?P<raw_status>Connection\s+closed)\s+by\s+authenticating\s+user\s+(?P<user>\S+)\s+(?P<ip_address>\d{1,3}(?:[-.]\d{1,3}){3})
    ''', re.VERBOSE),

    "received_disconnect": re.compile(r'''                                    #received_disconnect line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>\w+(?:\[\d*\])?):
    \s+(?P<raw_status>Received\s+disconnect)\s+from\s+(?P<ip_address>\d{1,3}(?:[-.]\d{1,3}){3})
    ''', re.VERBOSE),

    "disconnected": re.compile(r'''                                          #disconnected line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>\w+(?:\[\d*\])?):
    \s+(?P<raw_status>Disconnected)\s+from\s+(?:authenticating\s+)?(?:user\s+)?(?P<user>\S+)\s*?(?P<ip_address>\d{1,3}(?:[-.]\d{1,3}){3})
    ''', re.VERBOSE),

    "cron_pam_session": re.compile(r'''                                            #cron_pam_session line format V
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+(?P<service>CRON\[\d*\]):
    .*?
    (?P<raw_status>session\s*(?:opened|closed))
    \s+for\s+user\s+
    (?P<user>\S+)
    ''', re.VERBOSE),

    "authlog_unknown": re.compile(r'''                                                #unknown auth.log pattern
    (?P<timestamp>[a-zA-Z]{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})
    \s+ip-(?P<host>\d{1,3}(?:[-.]\d{1,3}){3})
    \s+
    (?P<message>.*)
    ''', re.VERBOSE)
}

###########################
# PATTERNS FOR access.log #
###########################

access_patterns = {                                          
    "access": re.compile(r'''                                    #access.log line format
    (?P<ip_address>\d{1,3}(?:\.\d{1,3}){3}).*\[
    (?P<timestamp>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4})\]\s+"
    (?P<method>\w+)\s+
    (?P<path>\S*)\s+
    (?P<protocol>HTTP[^"]+)"\s+
    (?P<status_code>\d{3})\s+
    (?P<response_size>\d+)
    (?:
    .*\s"
    (?P<referrer>[^"]*)"\s"
    (?P<user_agent>[^"]*)"
    )?.*
    ''', re.VERBOSE),  

    "accesslog_unknown": re.compile(r'''                                    #unknown access.log pattern
    (?P<ip_address>\d{1,3}(?:\.\d{1,3}){3}).*\[
    (?P<timestamp>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4})\]
    .*
    ''', re.VERBOSE)  
}

##########################
# PATTERNS FOR error.log #
##########################

error_patterns = {                                                     
    "error": re.compile(r'''                                    #error.log line format
    \[
    (?P<timestamp>\w{3}\s+\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2}.\d{6}\s+\d{4})\]\s+\[
    (?P<module>\w+):
    (?P<level>\w+)\]\s+\[pid\s+
    (?P<pid>\d+)(?:\:tid\s+
    (?P<tid>\d+))?\](?:\s+\[client\s+
    (?P<client_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):
    (?P<client_port>\d{1,5})\])?\s+
    (?P<error_code>\w+):\s+
    (?P<message>.*)
    ''', re.VERBOSE),

    "errorlog_unknown": re.compile(r'''                                    #unkown error.log pattern
    \[
    (?P<timestamp>\w{3}\s+\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2}.\d{6}\s+\d{4})\]
    .*
    ''', re.VERBOSE)  
}

##############################
# UNKNOWN PATTERN - fallback #
##############################

unknown_pattern = re.compile(r'''                                                #unknown pattern, fallback if no match in patterns
    (?P<err_message>.*)
    ''', re.VERBOSE)

