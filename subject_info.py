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
    
    Collects subject number, domain, valence, handedness, snack choice (if food domain), 
    and whether to run practice trials.
    Validates input (especially numeric subject ID) and creates a unique filename for data storage.
    
    Returns:
    dict
        Dictionary containing validated subject information:
        - subject_number (int): numeric ID for participant
        - domain (str): 'Money' or 'Food'
        - valence (str): 'Gain' or 'Loss'
        - handedness (str): 'Right' or 'Left'
        - snack_choice (str): chosen snack if Food domain, None if Money domain
        - practice_trials (bool): True if practice block is desired
        - filename (str): Unique filename for data storage
        - base_filename (str): Base filename for partial data naming
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
            
        # If validation passes, check for Food domain snack selection
        if domain == 'Food':
            snack_choice = None
            while True:  # Loop until snack is selected or user goes back
                snack_info = {
                    'Snack Choice': ['M&Ms', 'Cheez-Its', 'Nut Mix', 'Mini Pretzels', 'Mini Ritz', 'Gummi Bears']
                }
                
                snack_dlg = gui.DlgFromDict(
                    dictionary=snack_info,
                    title='Select Your Snack',
                    sortKeys=False
                )
                
                if not snack_dlg.OK:
                    logging.data('User cancelled snack selection - returning to main dialog')
                    snack_choice = None
                    break  # Break out of snack selection
                else:
                    snack_choice = snack_info['Snack Choice']
                    logging.data(f"[INFO] Snack selected: {snack_choice}")
                    break  # Break out of snack selection loop
            
            # If no snack was selected (user cancelled), go back to main dialog
            if snack_choice is None:
                continue  # Go back to beginning of main while loop
        else:
            snack_choice = None  # Money domain doesn't need snack selection
        
        break  # All validation and selection complete
    
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
    
    # Store the base name for partial file naming (without .csv extension)
    base_name_no_ext = f"{sub_num}_{domain_abbr}_{valence_abbr}"
    base_filename = f"{base_name_no_ext}_{counter}" if counter > 1 else base_name_no_ext

    logging.data(f"[INFO] Subject info collected: ID={sub_num}, domain={domain}, valence={valence}")

    if snack_choice:
        logging.data(f"[INFO] Snack choice: {snack_choice}")
    
    return {
        'subject_number': sub_num,
        'domain': domain,
        'valence': valence,
        'handedness': hand,
        'snack_choice': snack_choice,  # Will be None for Money domain
        'practice_trials': (practice == 'Yes'),
        'filename': filename,
        'base_filename': base_filename
    }