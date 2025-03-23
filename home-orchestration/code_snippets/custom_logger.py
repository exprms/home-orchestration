#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 05:54:33 2025

@author: bernd
"""

import logging

# Define ANSI color codes for different log levels
class Colors:
    
    GREEN = "\033[32m"   # Standard Green for INFO
    RED = "\033[91m"     # Standard Red for ERROR
    YELLOW = "\033[93m"  # Standard Yellow for WARNING
    RESET = "\033[0m"

# Define a custom formatter
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Color for the log level
        level_color = Colors.RESET
        message_color = Colors.RESET
        if record.levelno == logging.INFO:
            level_color = Colors.GREEN
            message_color = Colors.GREEN
        elif record.levelno == logging.ERROR:
            level_color = Colors.RED
            message_color = Colors.RED
        elif record.levelno == logging.WARNING:
            level_color = Colors.YELLOW
            message_color = Colors.YELLOW
        
        # Apply color to the log level and message
        log_level = f"{level_color}{record.levelname}{Colors.RESET}"
        log_message = f"{message_color}{record.msg}{Colors.RESET}"
        
        # Format the record with colored level and message
        record.levelname = log_level
        record.msg = log_message
        
        # Format the output string
        return super().format(record)

# Configure logger
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create colored formatter
formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(ch)

# Log messages of different levels
# logger.info('This is an info message.')
# logger.warning('This is a warning message.')
# logger.error('This is an error message.')