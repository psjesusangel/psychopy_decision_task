"""
utils.py
Module to set up experiment logging and save data to CSV.
"""
import os
import csv
from datetime import datetime
from psychopy import logging

def setup_logging(info=None, log_dir='logs'):
    """
    Configure PsychoPy logging system for experiment.
    
    Creates a log file matching the data file naming convention if info provided,
    otherwise uses timestamp.
    
    Parameters:
    info : dict, optional
        Subject information containing subject_number, domain, valence
    log_dir : str
        Directory where log files will be stored (created if not exists)
        
    Returns:
    str
        Path to the created log file
    """
    # Ensure log directory exists
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    
    # Generate filename based on subject info or timestamp
    if info and all(k in info for k in ['subject_number', 'domain', 'valence']):
        # Match data file naming convention
        sub_num = info['subject_number']
        domain_abbr = 'M' if info['domain'] == 'Money' else 'F'
        valence_abbr = 'G' if info['valence'] == 'Gain' else 'L'
        
        # Create base filename
        base_name = f"{sub_num}_{domain_abbr}_{valence_abbr}"
        log_filename = f"{log_dir}/{base_name}.log"
        
        # Handle duplicates
        counter = 1
        while os.path.exists(log_filename):
            log_filename = f"{log_dir}/{base_name}_{counter}.log"
            counter += 1
    else:
        # Fallback to timestamp if no info provided
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f"{log_dir}/experiment_{timestamp}.log"
    
    # Set up PsychoPy log file
    logging.LogFile(log_filename, level=logging.DATA)
    
    # Reduce console verbosity
    logging.console.setLevel(logging.WARNING)
    logging.data(f"[STRUCTURE] Logging initialized. Log file: {log_filename}")
    
    return log_filename

def create_data_file(filepath):
    """Create empty CSV file with headers."""
    headers = [
        'date', 'time', 'subject', 'handedness', 'trial_num', 
        'domain', 'valence', 'magnitude_hard', 'probability', 'EV',
        'choice', 'choice_rt', 'n_clicks_required', 'n_clicks_executed', 
        'task_complete', 'is_catch', 'trial_type'
    ]
    
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
    
    logging.data(f"[STRUCTURE] Data file created: {filepath}")

def append_trial_data(filepath, trial_data):
    """Append single trial data to existing CSV file."""
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=trial_data.keys())
        writer.writerow(trial_data)

def count_trials_in_file(filepath):
    """Count number of data rows in CSV file."""
    try:
        with open(filepath, 'r') as csvfile:
            return sum(1 for line in csvfile) - 1  # Subtract header row
    except FileNotFoundError:
        return 0