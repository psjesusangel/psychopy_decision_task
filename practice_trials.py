"""
practice_trials.py
Module for running practice trials in the effort-based decision task.
"""
import random
from psychopy import visual, event, core, logging
from config import PRACTICE_TRIALS

def run_practice_trials(win, info):
    """
    Run the practice trials for the effort-based decision task.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    info : dict
        Subject information including handedness and calibration data
        
    Returns:
    list
        List of dictionaries containing trial data
    """
    # Extract relevant information from info dictionary
    handedness = info['handedness']
    easy_clicks_required = info['easy_clicks_required']
    hard_clicks_required = info['hard_clicks_required']
    dominant_hand = handedness.upper()
    
    # Get non-dominant hand --> Consider moving to main later
    non_dominant_hand = "LEFT" if dominant_hand == "RIGHT" else "RIGHT"
    
    # List to store trial data
    practice_data = []
    
    # Run all three practice trials using config parameters
    for trial_num, trial_config in enumerate(PRACTICE_TRIALS, 1):
        trial_data = run_practice_trial(
            win, 
            trial_num, 
            trial_config['prob'], 
            trial_config['magnitude_hard'],
            non_dominant_hand,
            easy_clicks_required,
            hard_clicks_required
        )
        practice_data.append(trial_data)
    
    # Return data from practice trials
    return practice_data

def run_practice_trial(win, trial_num, probability, magnitude_hard, non_dominant_hand, easy_clicks_required, hard_clicks_required):
    """
    Run a single practice trial with given parameters.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    trial_num : int
        Trial number (1, 2, or 3)
    probability : float
        Probability of loss
    magnitude_hard : float
        Magnitude for the hard option
    non_dominant_hand : str
        The participant's non-dominant hand
    hard_clicks_required : int
        Number of clicks required for the hard task
        
    Returns:
    dict
        Dictionary containing trial data
    """
    # Initialize trial data dictionary
    trial_data = {
        'trial_num': trial_num,
        'trial_type': 'practice',
        'magnitude_hard': magnitude_hard,
        'probability': probability,
        'EV': magnitude_hard * probability,
        'choice': None,
        'choice_rt': None,
        'n_clicks_required': None,
        'n_clicks_executed': 0,
        'task_complete': 0
    }
    
    # Show fixation cross
    show_fixation(win, trial_num)
    
    # Show choice screen and get response
    choice, choice_rt = show_choice_screen(win, trial_num, probability, magnitude_hard)
    trial_data['choice'] = choice
    trial_data['choice_rt'] = choice_rt
    
    # Show ready screen
    show_ready_screen(win)
    
    # Execute the chosen task
    if choice == 'easy':
        task_complete, clicks_executed = run_easy_task(win, non_dominant_hand, easy_clicks_required, trial_num)
        trial_data['n_clicks_required'] = easy_clicks_required
    else:
        task_complete, clicks_executed = run_hard_task(win, non_dominant_hand, hard_clicks_required, trial_num)
        trial_data['n_clicks_required'] = hard_clicks_required
    
    trial_data['n_clicks_executed'] = clicks_executed
    trial_data['task_complete'] = 1 if task_complete else 0
    
    # Show task completion status
    show_completion_status(win, task_complete)
    
    return trial_data

def show_fixation(win, trial_num):
    """Show fixation cross with practice trial text."""
    fixation = visual.TextStim(win, text="+", height=0.08, color='white')
#    trial_text = visual.TextStim(
#        win, 
#        text=f"Practice trial\n{trial_num}", 
#        pos=(0, -0.15), 
#        height=0.05, 
#        color='white'
#    )
    
    fixation.draw()
    # trial_text.draw()
    win.flip()
    core.wait(1.0)

def show_choice_screen(win, trial_num, probability, magnitude_hard):
    """
    Display choice screen and get participant's response.
    
    Returns:
    (str, float)
        Tuple of (choice, reaction_time)
    """
    # Create visual elements
    elements = []
    
    # 5/28 Meeting: Remove headers
#    # Trial header
#    choice_text = visual.TextStim(
#        win,
#        text=f"Practice trial\n{trial_num}",
#        pos=(0, 0.35),
#        height=0.05,
#        color='white'
#    )
#    elements.append(choice_text)
    
    # Gray background box for choices
    choice_bg = visual.Rect(
        win,
        width=2.0, # was 1.4 but now fullscreen
        height=2.0, # was 0.5 but now fullscreen
        fillColor=[0.2, 0.2, 0.2], # dark gray
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
        text=f"Probability of loss: {int(probability * 100)}%",
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
    
    easy_value = visual.TextStim(
        win,
        text="-$4",
        pos=(-0.35, -0.20),
        height=0.04,
        color='black'
    )
    elements.append(easy_value)
    
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
    
    hard_value = visual.TextStim(
        win,
        text=f"-${magnitude_hard:.2f}",
        pos=(0.35, -0.20),
        height=0.04,
        color='black'
    )
    elements.append(hard_value)
    
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
        win.close()
        core.quit()
        
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

def show_ready_screen(win):
    """Display ready screen."""
    ready_text = visual.TextStim(
        win,
        text="Ready?",
        height=0.08,
        color='white'
    )
    ready_text.draw()
    win.flip()
    core.wait(1.0)

def show_completion_status(win, task_complete):
    """Display task completion status."""
    status_text = "complete" if task_complete else "incomplete"
    completion_text = visual.TextStim(
        win,
        text=f"Task {status_text}",
        height=0.08,
        color='white'
    )
    completion_text.draw()
    win.flip()
    core.wait(2.0) # TODO: 2 seconds feel a little long

def run_easy_task(win, non_dominant_hand, easy_clicks_required, trial_num):
    """
    Run the easy task (press space bar 30 times in 7 seconds).
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    non_dominant_hand : str
        The participant's non-dominant hand
    easy_clicks_required : int
        Number of clicks required for the hard task
    trial_num : int
        Trial number
        
    Returns:
    (bool, int)
        Tuple containing (task_complete, clicks_executed)
    """
    # Initialize variables
    clicks_executed = 0
    task_complete = False
    task_duration = 7.0  # 7 seconds for easy task
    
    # Create visual elements that don't change
    progress_bar_back = visual.Rect(
        win,
        width=0.1,
        height=0.6,
        fillColor='darkgrey',
        lineColor='white',
        pos=(0, 0)
    )
    
#    instruction_text = visual.TextStim(
#        win,
#        text=f"Practice trial {trial_num}\n(easy task)",
#        pos=(0, 0.4),
#        height=0.05,
#        color='white'
#    )
    
    task_text = visual.TextStim(
        win,
        text=f"Press the space bar with your {non_dominant_hand} index finger",
        pos=(0, -0.4),
        height=0.05,
        color='white'
    )
    
    # Clear any existing keypresses
    event.clearEvents()
    
    # Set up timer
    start_time = core.getTime()
    end_time = start_time + task_duration
    
    # Task loop
    while core.getTime() < end_time and clicks_executed < easy_clicks_required:
        # Check for keypresses
        keys = event.getKeys(keyList=['space', 'escape'])
        
        # Check for escape key
        if 'escape' in keys:
            win.close()
            core.quit()
            
        # Count spacebar presses
        if 'space' in keys:
            clicks_executed += 1
            
        # Calculate progress
        progress = min(1.0, clicks_executed / easy_clicks_required)
        new_height = 0.6 * progress
        
        # Update progress bar
        progress_bar_fill = visual.Rect(
            win,
            width=0.1,
            height=new_height,
            fillColor='blue',
            lineColor=None,
            pos=(0, -0.3 + new_height/2)
        )
        
        # Update progress text
        progress_text = visual.TextStim(
            win,
            text=f"{int(progress * 100)}%",
            pos=(0.15, 0),
            height=0.05,
            color='white'
        )
        
        # Update timer
        time_remaining = max(0, end_time - core.getTime())
        timer_text = visual.TextStim(
            win,
            text=f"{time_remaining:.1f}s",
            pos=(0.8, -0.8),
            height=0.04,
            color='white'
        )
        
        # Draw elements
        # instruction_text.draw()
        progress_bar_back.draw()
        progress_bar_fill.draw()
        progress_text.draw()
        task_text.draw()
        timer_text.draw()
        win.flip()
        
        # Brief wait to prevent CPU hogging
        core.wait(0.001)
    
    # Check if task was completed
    task_complete = clicks_executed >= easy_clicks_required
    
    return task_complete, clicks_executed

def run_hard_task(win, non_dominant_hand, hard_clicks_required, trial_num):
    """
    Run the hard task (press right and left arrow keys X times each in 21 seconds).
    Split into two slides: first RIGHT, then LEFT.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    non_dominant_hand : str
        The participant's non-dominant hand
    hard_clicks_required : int
        Number of clicks required for the hard task
    trial_num : int
        Trial number
        
    Returns:
    (bool, int)
        Tuple containing (task_complete, clicks_executed)
    """
    # Initialize variables
    right_clicks = 0
    left_clicks = 0
    task_duration = 21.0  # 21 seconds for hard task
    clicks_per_side = hard_clicks_required // 2  # Split between left and right
    
    # Clear any existing keypresses
    event.clearEvents()
    
    # Set up timer
    start_time = core.getTime()
    end_time = start_time + task_duration
    
    # Phase 1: RIGHT arrow key
    task_complete_right = execute_hard_task_phase(
        win, 'right', 'RIGHT', right_clicks, clicks_per_side, 
        trial_num, non_dominant_hand, end_time
    )
    right_clicks = task_complete_right[1]
    
    # Phase 2: LEFT arrow key (if time remains and right clicks completed)
    if right_clicks >= clicks_per_side and core.getTime() < end_time:
        task_complete_left = execute_hard_task_phase(
            win, 'left', 'LEFT', left_clicks, clicks_per_side,
            trial_num, non_dominant_hand, end_time
        )
        left_clicks = task_complete_left[1]
    
    # Calculate total clicks and completion status
    total_clicks = right_clicks + left_clicks
    task_complete = (right_clicks >= clicks_per_side and left_clicks >= clicks_per_side)
    
    return task_complete, total_clicks

def execute_hard_task_phase(win, key_name, key_display, current_clicks, required_clicks, 
                           trial_num, non_dominant_hand, end_time):
    """
    Execute one phase (LEFT or RIGHT) of the hard task.
    
    Returns:
    (bool, int)
        Tuple of (phase_complete, clicks_executed)
    """
    clicks = current_clicks
    
    # Create visual elements that don't change
    progress_bar_back = visual.Rect(
        win,
        width=0.1,
        height=0.6,
        fillColor='darkgrey',
        lineColor='white',
        pos=(0, 0)
    )
    
#    instruction_text = visual.TextStim(
#        win,
#        text=f"Practice trial {trial_num}\n(hard task)",
#        pos=(0, 0.4),
#        height=0.05,
#        color='white'
#    )
    
    task_text = visual.TextStim(
        win,
        text=f"Press the {key_display} arrow key with your {non_dominant_hand} pinky finger",
        pos=(0, -0.4),
        height=0.05,
        color='white'
    )
    
    while core.getTime() < end_time and clicks < required_clicks:
        # Check for keypresses
        keys = event.getKeys(keyList=[key_name, 'escape'])
        
        # Check for escape key
        if 'escape' in keys:
            win.close()
            core.quit()
            
        # Count arrow presses
        if key_name in keys:
            clicks += 1
        
        # Calculate progress
        progress = min(1.0, clicks / required_clicks)
        new_height = 0.6 * progress
        
        # Update progress bar
        progress_bar_fill = visual.Rect(
            win,
            width=0.1,
            height=new_height,
            fillColor='blue',
            lineColor=None,
            pos=(0, -0.3 + new_height/2)
        )
        
        # Update progress text
        progress_text = visual.TextStim(
            win,
            text=f"{int(progress * 100)}%",
            pos=(0.15, 0),
            height=0.05,
            color='white'
        )
        
        # Update timer
        time_remaining = max(0, end_time - core.getTime())
        timer_text = visual.TextStim(
            win,
            text=f"{time_remaining:.1f}s",
            pos=(0.8, -0.8),
            height=0.04,
            color='white'
        )
        
        # Draw elements
        # instruction_text.draw()
        progress_bar_back.draw()
        progress_bar_fill.draw()
        progress_text.draw()
        task_text.draw()
        timer_text.draw()
        win.flip()
        
        # Brief wait to prevent CPU hogging
        core.wait(0.001)
    
    phase_complete = clicks >= required_clicks
    return phase_complete, clicks