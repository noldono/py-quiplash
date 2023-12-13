"""
File: protocol.py
Author: Nolan Donovan (rndonovan@vt.edu)
Created: 4 November 2023
"""

""" To tell the client they need to send a response to a prompt, the PROMPT header is used """
PROMPT = "Prompt"

""" Client will respond to the server with a RESPONSE header indicating their response to a prompt """
RESPONSE = "Response"

""" Client will send a REGISTER message to the server with its unique username """
REGISTER = "Register"
