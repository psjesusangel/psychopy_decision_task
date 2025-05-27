"""
utils.py
Module to set up experiment logging and save data to CSV.
"""

import os
import csv
from datetime import datetime
from psychopy import logging

def setup_logging(log_dir='logs'):
    """
    Configure PsychoPy logging system for experiment.
    
    Creates a timestamped log file and configures console output levels.
    
    Parameters:
    log_dir : str
        Directory where log files will be stored (created if not exists)
        
    Returns:
    None
    """
    # Ensure log directory exists
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
        
    # Generate filename based on timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"{log_dir}/experiment_{timestamp}.log"
    
    # Set up PsychoPy log file
    logging.LogFile(log_filename, level=logging.DATA) # Upped to DATA from EXP
    
    # Reduce console verbosity
    logging.console.setLevel(logging.WARNING)
    logging.data(f"[STRUCTURE] Logging initialized. Log file: {log_filename}")

def save_data(filepath, data):
    """
    Save experimental data to a CSV file.
    
    Takes a list of dictionaries and saves as CSV with headers from dictionary keys.
    
    Parameters:
    filepath : str
        Destination path ending in .csv
    data : list
        List of dictionaries; each dict represents one row of data
        
    Returns:
    None
    """
    # If no data, warn and exit
    if not data:
        logging.warning("save_data called with empty data list.")
        return
        
    # Ensure parent directory exists
    parent_dir = os.path.dirname(filepath)
    if parent_dir and not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)
        
    # Write CSV
    with open(filepath, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(data[0].keys()))
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
    logging.data(f"[STRUCTURE] Data saved to {filepath}")