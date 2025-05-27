"""
subject_info.py
Module to collect and validate participant information via PsychoPy GUI.
"""

import os
from datetime import datetime
from psychopy import gui, logging, core

def get_subject_info():
    """
    Collect and validate subject information through a GUI dialog.
    
    Collects subject number, domain, valence, handedness, and whether to run practice trials.
    Validates input (especially numeric subject ID) and creates a unique filename for data storage.
    
    Returns:
    dict
        Dictionary containing validated subject information:
        - subject_number (int): numeric ID for participant
        - domain (str): 'Money' or 'Food'
        - valence (str): 'Gain' or 'Loss'
        - handedness (str): 'Right' or 'Left'
        - practice_trials (bool): True if practice block is desired
        - filename (str): Unique filename for data storage
    """
    # Loop until all entries are valid (or user cancels)
    while True:
        # Define a fresh info dictionary for each iteration
        # Using lists as values creates dropdown menus in older PsychoPy versions
        info = {
            'Subject Number': '',
            'Domain': ['Money', 'Food'],
            'Valence': ['Gain', 'Loss'],
            'Handedness': ['Right', 'Left'],
            'Practice Trials?': ['Yes', 'No']
        }
        
        # Create dialog
        dlg = gui.DlgFromDict(
            dictionary=info,
            title='Participant Information',
            sortKeys=False
        )
        
        if not dlg.OK:
            logging.error('User cancelled participant info dialog.')
            core.quit()
        
        # Strip and extract
        snum = info['Subject Number'].strip()
        domain = info['Domain']
        valence = info['Valence']
        hand = info['Handedness']
        practice = info['Practice Trials?']
        
        # Validate
        errors = []
        
        if not snum:
            errors.append("Subject Number is required")
        elif not snum.isdigit():
            errors.append("Subject Number must contain only digits")
        
        # Only show an error dialog if there are errors
        if errors:
            alert = gui.Dlg(title='Input Error')
            for error in errors:
                alert.addText(error)
            alert.addText("\nPress OK to try again")
            alert.show()
            continue  # Re-display the main dialog
            
        break  # All good
    
    # Convert and finalize
    sub_num = int(snum)
    domain_abbr = 'M' if domain == 'Money' else 'F'
    valence_abbr = 'G' if valence == 'Gain' else 'L'
    
    # Create filename following spec: [subject number]_[domain]_[valence].csv
    base_name = f"{sub_num}_{domain_abbr}_{valence_abbr}.csv"
    filename = base_name
    counter = 1
    
    # Avoid overwrite by appending 1, 2, etc.
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    while os.path.exists(os.path.join(data_dir, filename)):
        filename = f"{sub_num}_{domain_abbr}_{valence_abbr}_{counter}.csv"
        counter += 1
    
    logging.data(f"[INFO] Subject info collected: ID={sub_num}, domain={domain}, valence={valence}")
    
    return {
        'subject_number': sub_num,
        'domain': domain,
        'valence': valence,
        'handedness': hand,
        'practice_trials': (practice == 'Yes'),
        'filename': filename
    }