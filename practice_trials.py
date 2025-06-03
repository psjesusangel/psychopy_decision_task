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
    domain = info['domain']
    valence = info['valence']
    dominant_hand = handedness.upper()
    
    # Get non-dominant hand
    non_dominant_hand = "LEFT" if dominant_hand == "RIGHT" else "RIGHT"
    
    # Run all three practice trials using config parameters
    for trial_num, trial_config in enumerate(PRACTICE_TRIALS, 1):
        run_practice_trial(
            win, 
            trial_num, 
            trial_config['prob'], 
            trial_config['magnitude_hard'],
            non_dominant_hand,
            easy_clicks_required,
            hard_clicks_required,
            domain,
            valence
        )

def run_practice_trial(win, trial_num, probability, magnitude_hard, non_dominant_hand, easy_clicks_required, hard_clicks_required, domain, valence):
    """
    Run a single practice trial with given parameters.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    trial_num : int
        Trial number (1, 2, or 3)
    probability : float
        Probability of loss/gain
    magnitude_hard : float
        Magnitude for the hard option
    non_dominant_hand : str
        The participant's non-dominant hand
    easy_clicks_required : int
        Number of clicks required for easy task
    hard_clicks_required : int
        Number of clicks required for the hard task
    domain : str
        'Money' or 'Food'
    valence : str
        'Gain' or 'Loss'
        
    Returns:
    dict
        Dictionary containing trial data
    """
    # Show fixation cross
    show_fixation(win)
    
    # Show choice screen and get response
    choice, choice_rt = show_choice_screen(win, probability, magnitude_hard, domain, valence)
    
    # Show ready screen
    show_ready_screen(win)
    
    # Execute the chosen task
    if choice == 'easy':
        task_complete, clicks_executed = run_easy_task(win, non_dominant_hand, easy_clicks_required)
    else:
        task_complete, clicks_executed = run_hard_task(win, non_dominant_hand, hard_clicks_required)
    
    # Show task completion status
    show_completion_status(win, task_complete)

def show_fixation(win):
    """Show fixation cross."""
    fixation = visual.TextStim(win, text="+", height=0.08, color='white')
    fixation.draw()
    win.flip()
    core.wait(1.0)

def show_choice_screen(win, probability, magnitude_hard, domain, valence):
    """
    Display choice screen and get participant's response.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    probability : float
        Probability of loss/gain
    magnitude_hard : float
        Magnitude for hard option
    domain : str
        'Money' or 'Food'
    valence : str
        'Gain' or 'Loss'
    
    Returns:
    (str, float)
        Tuple of (choice, reaction_time)
    """
    # Set correct easy values and display format based on valence
    if valence == 'Loss':
        easy_value = 4.00
        if domain == 'Money':
            easy_display = f"-${easy_value:.2f}"
            hard_display = f"-${magnitude_hard:.2f}"
            prob_label = f"Probability of loss: {int(probability * 100)}%"
        else:  # Food
            easy_display = f"-{int(easy_value)}"
            hard_display = f"-{int(magnitude_hard)}"
            prob_label = f"Probability of loss: {int(probability * 100)}%"
    else:  # Gain
        easy_value = 1.00
        if domain == 'Money':
            easy_display = f"+${easy_value:.2f}"
            hard_display = f"+${magnitude_hard:.2f}"
            prob_label = f"Probability of gain: {int(probability * 100)}%"
        else:  # Food
            easy_display = f"+{int(easy_value)}"
            hard_display = f"+{int(magnitude_hard)}"
            prob_label = f"Probability of gain: {int(probability * 100)}%"
    
    # Create visual elements
    elements = []
    
    # Gray background box for choices - full screen
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
    
    easy_value_display = visual.TextStim(
        win,
        text=easy_display,
        pos=(-0.35, -0.20),
        height=0.04,
        color='black'
    )
    elements.append(easy_value_display)
    
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
    
    hard_value_display = visual.TextStim(
        win,
        text=hard_display,
        pos=(0.35, -0.20),
        height=0.04,
        color='black'
    )
    elements.append(hard_value_display)
    
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
        raise KeyboardInterrupt("User pressed escape during practice trial")
        
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
    core.wait(2.0)

def run_easy_task(win, non_dominant_hand, easy_clicks_required):
    """
    Run the easy task (press space bar X times in 7 seconds).
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    non_dominant_hand : str
        The participant's non-dominant hand
    easy_clicks_required : int
        Number of clicks required for the easy task
        
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
            raise KeyboardInterrupt("User pressed escape during easy task")
            
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

def run_hard_task(win, non_dominant_hand, hard_clicks_required):
    """
    Run the hard task (press right and left arrow keys X times each in 21 seconds).
    Split into two phases: first RIGHT, then LEFT.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    non_dominant_hand : str
        The participant's non-dominant hand
    hard_clicks_required : int
        Number of clicks required for the hard task
        
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
        non_dominant_hand, end_time
    )
    right_clicks = task_complete_right[1]
    
    # Phase 2: LEFT arrow key (if time remains and right clicks completed)
    if right_clicks >= clicks_per_side and core.getTime() < end_time:
        task_complete_left = execute_hard_task_phase(
            win, 'left', 'LEFT', left_clicks, clicks_per_side,
            non_dominant_hand, end_time
        )
        left_clicks = task_complete_left[1]
    
    # Calculate total clicks and completion status
    total_clicks = right_clicks + left_clicks
    task_complete = (right_clicks >= clicks_per_side and left_clicks >= clicks_per_side)
    
    return task_complete, total_clicks

def execute_hard_task_phase(win, key_name, key_display, current_clicks, required_clicks, 
                           non_dominant_hand, end_time):
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
            raise KeyboardInterrupt("User pressed escape during hard task")
            
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