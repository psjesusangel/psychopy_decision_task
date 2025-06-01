"""
real_trials.py
Module for running the main experimental trials in the effort-based decision task.
"""
import random
from datetime import datetime
from psychopy import visual, event, core, logging
from config import (
    MONEY_MAGNITUDES, FOOD_MAGNITUDES, PROBABILITIES, ITI_RANGE,
    N_REAL_TRIALS, N_CATCH_TRIALS, CATCH_TRIAL_CONFIGS,
    LOSS_EASY_VALUE, LOSS_HARD_VALUE, GAIN_EASY_VALUE, GAIN_HARD_VALUE
)
from practice_trials import (
    show_fixation, show_ready_screen, show_completion_status,
    run_easy_task, run_hard_task
)
from utils import append_trial_data

def run_real_trials(win, info):
    """
    Run the main experimental trials.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    info : dict
        Subject information including domain, valence, handedness, etc.
        
    Returns:
    list
        List of dictionaries containing trial data
    """
    # Extract relevant information
    domain = info['domain']
    valence = info['valence'] 
    handedness = info['handedness']
    easy_clicks_required = info['easy_clicks_required']
    hard_clicks_required = info['hard_clicks_required']
    subject_number = info['subject_number']
    
    # Get non-dominant hand
    dominant_hand = handedness.upper()
    non_dominant_hand = "LEFT" if dominant_hand == "RIGHT" else "RIGHT"
    
    # Generate trial list
    trial_list = generate_trial_list(domain, valence)
    
    # Randomize trial order
    random.shuffle(trial_list)
    
    # List to store trial data
    trial_data_list = []
    
    # Show initial experiment screen
    show_experiment_start(win)
    
    # Run all trials
    try: 
        for trial_num, trial_params in enumerate(trial_list, 1):
            # Show fixation with ITI
            show_trial_fixation(win, trial_num)
            
            # Run the trial
            trial_data = run_single_trial(
                win, 
                trial_num,
                trial_params,
                domain,
                valence,
                non_dominant_hand,
                easy_clicks_required, 
                hard_clicks_required,
                subject_number,
                handedness
            )
            
            # Save trial data immediately
            append_trial_data(info['data_file_path'], trial_data)
            
            # Add trial data to list
            trial_data_list.append(trial_data)
            
            # Inter-trial interval
            iti = random.uniform(*ITI_RANGE)
            core.wait(iti)
            
    except KeyboardInterrupt:
        # User pressed escape during trials -> let main.py handle the partial file renaming
        logging.data(f"[STRUCTURE] User interrupted during trial {trial_num}")
        raise  # Re-raise to let main.py handle it
        
    return trial_data_list

def generate_trial_list(domain, valence):
    """
    Generate list of trial parameters based on domain and valence.
    
    Parameters:
    domain : str
        'Money' or 'Food'
    valence : str
        'Gain' or 'Loss'
        
    Returns:
    list
        List of dictionaries containing trial parameters
    """
    trial_list = []
    
    # Generate regular trials
    if domain == 'Money':
        # For money: Create all possible combinations
        all_combinations = []
        for mag in MONEY_MAGNITUDES:
            for prob in PROBABILITIES:
                all_combinations.append({
                    'magnitude_hard': mag,
                    'probability': prob,
                    'is_catch': False
                })
        
        # Randomly select 39 trials (since we have 45 combinations)
        # But we need to ensure we actually have enough combinations
        num_trials_needed = min(N_REAL_TRIALS, len(all_combinations))
        regular_trials = random.sample(all_combinations, num_trials_needed)
        trial_list.extend(regular_trials)
        
    else:  # Food
        # For food: Need to repeat to get to 39 trials
        # Each combination appears ~3 times (39 / 12 ≈ 3.25)
        base_combinations = []
        for mag in FOOD_MAGNITUDES:
            for prob in PROBABILITIES:
                base_combinations.append({
                    'magnitude_hard': mag,
                    'probability': prob,
                    'is_catch': False
                })
        
        # Repeat combinations to reach 39 trials
        regular_trials = []
        full_repeats = N_REAL_TRIALS // len(base_combinations)
        remainder = N_REAL_TRIALS % len(base_combinations)
        
        # Add full repeats
        for _ in range(full_repeats):
            regular_trials.extend(base_combinations)
        
        # Add remainder
        regular_trials.extend(random.sample(base_combinations, remainder))
        
        trial_list.extend(regular_trials)
    
    # Add catch trials
    catch_config = CATCH_TRIAL_CONFIGS[valence]
    for _ in range(N_CATCH_TRIALS):
        trial_list.append({
            'magnitude_hard': catch_config['hard_value'],
            'probability': catch_config['probability'],
            'is_catch': True
        })
    
    return trial_list

def show_experiment_start(win):
    """Show experiment start screen."""
    start_text = visual.TextStim(
        win,
        text="+\n\nExperiment",
        height=0.06,
        color='white'
    )
    start_text.draw()
    win.flip()
    core.wait(1.0)

def show_trial_fixation(win, trial_num):
    """Show fixation cross for experimental trials."""
    fixation = visual.TextStim(win, text="+", height=0.08, color='white')
    fixation.draw()
    win.flip()
    # Note: ITI is handled in main loop, this is just the fixation display

def run_single_trial(win, trial_num, trial_params, domain, valence, 
                    non_dominant_hand, easy_clicks_required, hard_clicks_required, subject_number, handedness):
    """
    Run a single experimental trial.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    trial_num : int
        Trial number
    trial_params : dict
        Parameters for this trial (magnitude, probability, is_catch)
    domain : str
        'Money' or 'Food'
    valence : str
        'Gain' or 'Loss'
    non_dominant_hand : str
        Participant's non-dominant hand
    easy_clicks_required: int
        Number of clicks required for easy task
    hard_clicks_required : int
        Number of clicks required for hard task
    subject_number : int
        Subject ID
    handedness : str
        Participant's handedness
        
    Returns:
    dict
        Dictionary containing all trial data
    """
    # Extract trial parameters
    magnitude_hard = trial_params['magnitude_hard']
    probability = trial_params['probability']
    is_catch = trial_params['is_catch']
    
    # Set up values based on valence
    if valence == 'Loss':
        easy_value = LOSS_EASY_VALUE
        if is_catch:
            # For catch trials, hard value equals easy value
            magnitude_hard = easy_value
    else:  # Gain
        easy_value = GAIN_EASY_VALUE
        if is_catch:
            # For catch trials, hard value equals easy value
            magnitude_hard = easy_value
    
    # Calculate expected value
    ev = magnitude_hard * probability
    
    # Initialize trial data
    trial_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M:%S'),
        'subject': subject_number,
        'handedness': handedness,
        'trial_num': trial_num,
        'domain': domain,
        'valence': valence,
        'magnitude_hard': magnitude_hard,
        'probability': probability,
        'EV': ev,
        'choice': None,
        'choice_rt': None,
        'n_clicks_required': None,
        'n_clicks_executed': 0,
        'task_complete': 0,
        'is_catch': int(is_catch)
    }
    
    # Show choice screen and get response
    choice, choice_rt = show_experiment_choice_screen(
        win, probability, magnitude_hard, easy_value, domain, valence
    )
    trial_data['choice'] = choice
    trial_data['choice_rt'] = choice_rt
    
    # Show ready screen
    show_ready_screen(win)
    
    # Execute the chosen task
    if choice == 'easy':
        task_complete, clicks_executed = run_easy_task(win, non_dominant_hand, easy_clicks_required, None)
        trial_data['n_clicks_required'] = easy_clicks_required
    else:
        task_complete, clicks_executed = run_hard_task(win, non_dominant_hand, hard_clicks_required, None)
        trial_data['n_clicks_required'] = hard_clicks_required
    
    trial_data['n_clicks_executed'] = clicks_executed
    trial_data['task_complete'] = 1 if task_complete else 0
    
    # Show task completion status
    show_completion_status(win, task_complete)
    
    # Log catch trial responses
    if is_catch and choice == 'hard':
        logging.data(f"[CATCH TRIAL] Participant chose hard option on catch trial {trial_num}")
    
    return trial_data

def show_experiment_choice_screen(win, probability, magnitude_hard, easy_value, domain, valence):
    """
    Display choice screen for experimental trials with proper formatting for domain/valence.
    
    Returns:
    (str, float)
        Tuple of (choice, reaction_time)
    """
    # Format values based on domain and valence
    if domain == 'Money':
        if valence == 'Loss':
            easy_display = f"-${easy_value:.2f}"
            hard_display = f"-${magnitude_hard:.2f}"
        else:  # Gain
            easy_display = f"+${easy_value:.2f}"
            hard_display = f"+${magnitude_hard:.2f}"
    else:  # Food
        if valence == 'Loss':
            easy_display = f"-{int(easy_value)}"
            hard_display = f"-{int(magnitude_hard)}"
        else:  # Gain
            easy_display = f"+{int(easy_value)}"
            hard_display = f"+{int(magnitude_hard)}"
    
    # Set probability label based on valence
    prob_label = f"Probability of {'loss' if valence == 'Loss' else 'gain'}: {int(probability * 100)}%"
    
    # Create visual elements
    elements = []
    
    # 5/28 Meeting: Remove headers
#    # "Experiment" header
#    header_text = visual.TextStim(
#        win,
#        text="Experiment",
#        pos=(0, 0.35),
#        height=0.05,
#        color='white'
#    )
#    elements.append(header_text)
    
    # Gray background box for FULL background
    choice_bg = visual.Rect(
        win,
        width=2.0,
        height=2.0,
        fillColor=[0.2, 0.2, 0.2],
        pos=(0, 0)
    )
    elements.append(choice_bg)
    
    # "Please choose a task:" text
    instructions = visual.TextStim(
        win,
        text="Please choose a task:",
        pos=(0, 0.1),
        height=0.04,
        color='white'
    )
    elements.append(instructions)
    
    # Probability text
    probability_text = visual.TextStim(
        win,
        text=prob_label,
        pos=(0, 0.0),
        height=0.035,
        color='white'
    )
    elements.append(probability_text)
    
    # Easy option box
    easy_box = visual.Rect(
        win,
        width=0.35,
        height=0.18,
        fillColor=[0.6, 0.6, 0.6],
        lineColor='white',
        lineWidth=1,
        pos=(-0.35, -0.15)
    )
    elements.append(easy_box)
    
    easy_label = visual.TextStim(
        win,
        text="Easy",
        pos=(-0.35, -0.10),
        height=0.035,
        color='black',
        bold=True
    )
    elements.append(easy_label)
    
    easy_value_text = visual.TextStim(
        win,
        text=easy_display,
        pos=(-0.35, -0.20),
        height=0.04,
        color='black'
    )
    elements.append(easy_value_text)
    
    easy_key = visual.TextStim(
        win,
        text="(left arrow key)",
        pos=(-0.35, -0.28),
        height=0.025,
        color='white'
    )
    elements.append(easy_key)
    
    # Hard option box
    hard_box = visual.Rect(
        win,
        width=0.35,
        height=0.18,
        fillColor=[0.6, 0.6, 0.6],
        lineColor='white',
        lineWidth=1,
        pos=(0.35, -0.15)
    )
    elements.append(hard_box)
    
    hard_label = visual.TextStim(
        win,
        text="Hard",
        pos=(0.35, -0.10),
        height=0.035,
        color='black',
        bold=True
    )
    elements.append(hard_label)
    
    hard_value_text = visual.TextStim(
        win,
        text=hard_display,
        pos=(0.35, -0.20),
        height=0.04,
        color='black'
    )
    elements.append(hard_value_text)
    
    hard_key = visual.TextStim(
        win,
        text="(right arrow key)",
        pos=(0.35, -0.28),
        height=0.025,
        color='white'
    )
    elements.append(hard_key)
    
    # Draw all elements
    for element in elements:
        element.draw()
    win.flip()
    
    # Wait for response and record time
    choice_start_time = core.getTime()
    choice_keys = event.waitKeys(keyList=['left', 'right', 'escape'])
    choice_end_time = core.getTime()
    
    # Check for escape key
    if 'escape' in choice_keys:
        logging.warning('User pressed escape during experiment')
        raise KeyboardInterrupt("User pressed escape during trial")
        
    # Record choice and reaction time
    choice = 'easy' if choice_keys[0] == 'left' else 'hard'
    choice_rt = choice_end_time - choice_start_time
    
    # Show confirmation with red border
    border_box = visual.Rect(
        win,
        width=0.35,
        height=0.18,
        fillColor=None,
        lineColor='red',
        lineWidth=3,
        pos=(-0.35, -0.15) if choice == 'easy' else (0.35, -0.15)
    )
    
    # Redraw everything with highlight
    for element in elements:
        element.draw()
    border_box.draw()
    win.flip()
    
    # Brief pause to show selection
    core.wait(0.5)
    
    return choice, choice_rt