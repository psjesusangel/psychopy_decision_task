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

def save_data(filepath, data_list):
    """
    Save experimental data to CSV file.
    
    Parameters:
    filepath : str
        Full path to save the CSV file
    data_list : list
        List of dictionaries containing trial data
    """    
    if not data_list:
        logging.warning("No data to save")
        return
    
    # Get all unique keys from all trials
    all_keys = set()
    for trial in data_list:
        all_keys.update(trial.keys())
    
    # Define column order
    column_order = [
        'date', 'time', 'subject', 'handedness', 'trial_num', 
        'domain', 'valence', 'magnitude_hard', 'probability', 'EV',
        'choice', 'choice_rt', 'n_clicks_required', 'n_clicks_executed', 
        'task_complete', 'is_catch', 'trial_type'
    ]
    
    # Add any remaining keys not in column_order
    remaining_keys = all_keys - set(column_order)
    column_order.extend(sorted(remaining_keys))
    
    # Filter to only include keys that exist in the data
    actual_columns = [col for col in column_order if col in all_keys]
    
    # Write to CSV
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=actual_columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data_list)
    
    logging.data(f"[STRUCTURE] Data saved to {filepath} with {len(data_list)} trials")

def save_partial_data(info, all_data, reason="User quit"):
    """
    Save partial data when experiment is terminated early.
    
    Parameters:
    info : dict
        Subject information
    all_data : list
        List of trial data collected so far
    reason : str
        Reason for early termination
    """
    if not all_data:
        logging.warning("No data to save (experiment ended before any trials)")
        return
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Modify filename to indicate partial data
    original_filename = info['filename']
    base, ext = os.path.splitext(original_filename)
    partial_filename = f"{base}_PARTIAL{ext}"
    output_path = os.path.join(data_dir, partial_filename)
    
    # Add termination info to last trial
    if all_data:
        all_data[-1]['termination_reason'] = reason
        all_data[-1]['partial_data'] = True
    
    # Save the data
    save_data(output_path, all_data)
    logging.data(f"[STRUCTURE] Partial data saved to {output_path} - Reason: {reason}")
    
    return output_path