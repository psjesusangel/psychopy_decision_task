"""
practice_trials.py
Module for running practice trials in the effort-based decision task.
"""
import random
from psychopy import visual, event, core, logging
from config import EASY_CLICKS_REQUIRED

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
    hard_clicks_required = info['hard_clicks_required']
    dominant_hand = handedness.upper()
    
    # Get non-dominant hand
    non_dominant_hand = "LEFT" if dominant_hand == "RIGHT" else "RIGHT"
    
    # List to store trial data
    practice_data = []
    
    # Run first practice trial
    trial_data = run_practice_trial_1(win, non_dominant_hand, hard_clicks_required)
    practice_data.append(trial_data)
    
    # Run second practice trial
    
    # Run third practice trial
    
    # Return data from practice trials
    return practice_data

def run_practice_trial_1(win, non_dominant_hand, hard_clicks_required):
    """
    Run the first practice trial.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    non_dominant_hand : str
        The participant's non-dominant hand
    hard_clicks_required : int
        Number of clicks required for the hard task
        
    Returns:
    dict
        Dictionary containing trial data
    """
    # Set up trial parameters
    trial_num = 1
    probability = 0.88
    magnitude_hard = 1.00
    
    # Initialize trial data dictionary
    trial_data = {
        'trial_num': trial_num,
        'magnitude_hard': magnitude_hard,
        'probability': probability,
        'EV': magnitude_hard * probability,
        'choice': None,
        'choice_rt': None,
        'n_clicks_required': None,
        'n_clicks_executed': 0,
        'task_complete': 0
    }
    
    # Step 1: Fixation Cross with Practice Trial text
    fixation = visual.TextStim(win, text="+", height=0.08, color='white')
    trial_text = visual.TextStim(
        win, 
        text=f"Practice trial\n{trial_num}", 
        pos=(0, -0.15), 
        height=0.05, 
        color='white'
    )
    
    # Draw fixation cross and trial text
    fixation.draw()
    trial_text.draw()
    win.flip()
    
    # Wait for 1 second
    core.wait(1.0)
    
    # Step 2: Choice screen
    choice_text = visual.TextStim(
        win,
        text=f"Practice trial\n{trial_num}",
        pos=(0, 0.3),
        height=0.05,
        color='white'
    )
    
    instructions = visual.TextStim(
        win,
        text="Please choose a task:",
        pos=(0, 0.2),
        height=0.05,
        color='white'
    )
    
    left_key_text = visual.TextStim(
        win,
        text="(left arrow key)",
        pos=(-0.3, -0.1),
        height=0.03,
        color='white'
    )
    
    right_key_text = visual.TextStim(
        win,
        text="(right arrow key)",
        pos=(0.3, -0.1),
        height=0.03,
        color='white'
    )
    
    probability_text = visual.TextStim(
        win,
        text=f"Probability of loss: {int(probability * 100)}%",
        pos=(0, -0.2),
        height=0.04,
        color='white'
    )
    
    easy_option = visual.TextStim(
        win,
        text="Easy\n-$4",
        pos=(-0.3, 0),
        height=0.05,
        color='white'
    )
    
    hard_option = visual.TextStim(
        win,
        text=f"Hard\n-${magnitude_hard:.2f}",
        pos=(0.3, 0),
        height=0.05,
        color='white'
    )
    
    # Draw choice screen
    choice_text.draw()
    instructions.draw()
    left_key_text.draw()
    right_key_text.draw()
    probability_text.draw()
    easy_option.draw()
    hard_option.draw()
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

    trial_data['choice'] = choice
    trial_data['choice_rt'] = choice_rt

    # Confirmation highlight
    border_box = visual.Rect(
        win,
        width=0.35,
        height=0.18,
        lineColor='red',
        lineWidth=4,
        pos=(-0.3, 0) if choice == 'easy' else (0.3, 0)
    )

    # Redraw same screen with highlight
    choice_text.draw()
    instructions.draw()
    left_key_text.draw()
    right_key_text.draw()
    probability_text.draw()
    easy_option.draw()
    hard_option.draw()
    border_box.draw()
    win.flip()

    # Wait for 1 second to confirm selection visually
    core.wait(1.0)

    # Step 3: Ready screen
    ready_text = visual.TextStim(
        win,
        text="Ready?",
        height=0.08,
        color='white'
    )
    
    ready_text.draw()
    win.flip()
    
    # Wait for 1 second
    core.wait(1.0)
    
    # Step 4: Execute the chosen task
    if choice == 'easy':
        task_complete, clicks_executed = run_easy_task(win, non_dominant_hand, trial_num)
        trial_data['n_clicks_required'] = EASY_CLICKS_REQUIRED
    else:
        task_complete, clicks_executed = run_hard_task(win, non_dominant_hand, hard_clicks_required, trial_num)
        trial_data['n_clicks_required'] = hard_clicks_required
    
    trial_data['n_clicks_executed'] = clicks_executed
    trial_data['task_complete'] = 1 if task_complete else 0
    
    # Step 5: Show task completion status
    status_text = "complete" if task_complete else "incomplete"
    completion_text = visual.TextStim(
        win,
        text=f"Task {status_text}",
        height=0.08,
        color='white'
    )
    
    completion_text.draw()
    win.flip()
    
    # Wait for 2 seconds
    core.wait(2.0)
    
    return trial_data

def run_easy_task(win, non_dominant_hand, trial_num):
    """
    Run the easy task (press space bar 30 times in 7 seconds).
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    non_dominant_hand : str
        The participant's non-dominant hand
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
    
    # Create VERTICAL progress bar (shorter)
    progress_bar_back = visual.Rect(
        win,
        width=0.1,
        height=0.6,  # Shortened from 0.8
        fillColor='darkgrey',
        lineColor='white',
        pos=(0, 0)
    )
    
    progress_bar_fill = visual.Rect(
        win,
        width=0.1,
        height=0,  # Starts at 0
        fillColor='blue',
        lineColor=None,
        pos=(0, -0.3),  # Bottom-aligned (adjusted for shorter bar)
    )
    
    # Create instruction text
    instruction_text = visual.TextStim(
        win,
        text=f"Practice trial {trial_num}\n(easy task)",
        pos=(0, 0.4),  # Adjusted position
        height=0.05,
        color='white'
    )
    
    progress_text = visual.TextStim(
        win,
        text="0%",
        pos=(0.15, 0),  # To the right of bar
        height=0.05,
        color='white'
    )
    
    task_text = visual.TextStim(
        win,
        text=f"Press the space bar with your {non_dominant_hand} index finger",
        pos=(0, -0.4),  # Adjusted position
        height=0.05,
        color='white'
    )
    
    # Create timer text (bottom right corner)
    timer_text = visual.TextStim(
        win,
        text=f"{task_duration:.1f}s",
        pos=(0.8, -0.8),  # Bottom right corner
        height=0.04,
        color='white'
    )
    
    # Clear any existing keypresses
    event.clearEvents()
    
    # Set up timer
    start_time = core.getTime()
    end_time = start_time + task_duration
    
    # Task loop
    while core.getTime() < end_time and clicks_executed < EASY_CLICKS_REQUIRED:
        # Check for keypresses
        keys = event.getKeys(keyList=['space', 'escape'])
        
        # Check for escape key
        if 'escape' in keys:
            win.close()
            core.quit()
            
        # Count spacebar presses
        if 'space' in keys:
            clicks_executed += 1
            
        # Calculate progress (0 to 1)        
        progress = min(1.0, clicks_executed / EASY_CLICKS_REQUIRED)
        new_height = 0.6 * progress  # Adjusted for shorter bar
        
        # Update progress bar (grows from bottom to top)
        progress_bar_fill.height = new_height
        progress_bar_fill.pos = (0, -0.3 + new_height/2)  # Adjust y position as it grows
        
        # Update progress text
        progress_text.text = f"{int(progress * 100)}%"
        
        # Update timer
        time_remaining = max(0, end_time - core.getTime())
        timer_text.text = f"{time_remaining:.1f}s"
        
        # Draw elements
        instruction_text.draw()
        progress_bar_back.draw()
        progress_bar_fill.draw()
        progress_text.draw()
        task_text.draw()
        timer_text.draw()
        win.flip()
        
        # Brief wait to prevent CPU hogging
        core.wait(0.001)
    
    # Check if task was completed
    task_complete = clicks_executed >= EASY_CLICKS_REQUIRED
    
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
    total_clicks = 0
    task_complete = False
    task_duration = 21.0  # 21 seconds for hard task
    clicks_per_side = hard_clicks_required // 2  # Split between left and right
    
    # Clear any existing keypresses
    event.clearEvents()
    
    # Set up timer
    start_time = core.getTime()
    end_time = start_time + task_duration
    
    # Phase 1: RIGHT arrow key
    while core.getTime() < end_time and right_clicks < clicks_per_side:
        # Create VERTICAL progress bar (shorter)
        progress_bar_back = visual.Rect(
            win,
            width=0.1,
            height=0.6,  # Shortened from 0.8
            fillColor='darkgrey',
            lineColor='white',
            pos=(0, 0)
        )
        
        progress_bar_fill = visual.Rect(
            win,
            width=0.1,
            height=0.6 * (right_clicks / clicks_per_side),
            fillColor='blue',
            lineColor=None,
            pos=(0, -0.3 + (0.6 * (right_clicks / clicks_per_side) / 2)),
            anchor='center'
        )
        
        # Create instruction text
        instruction_text = visual.TextStim(
            win,
            text=f"Practice trial {trial_num}\n(hard task)",
            pos=(0, 0.4),
            height=0.05,
            color='white'
        )
        
        progress_text = visual.TextStim(
            win,
            text=f"{int((right_clicks / clicks_per_side) * 100)}%",
            pos=(0.15, 0),
            height=0.05,
            color='white'
        )
        
        task_text = visual.TextStim(
            win,
            text=f"Press the RIGHT arrow key with your {non_dominant_hand} pinky finger",
            pos=(0, -0.4),
            height=0.05,
            color='white'
        )
        
        # Create timer text (bottom right corner)
        time_remaining = max(0, end_time - core.getTime())
        timer_text = visual.TextStim(
            win,
            text=f"{time_remaining:.1f}s",
            pos=(0.8, -0.8),
            height=0.04,
            color='white'
        )
        
        # Draw elements
        instruction_text.draw()
        progress_bar_back.draw()
        progress_bar_fill.draw()
        progress_text.draw()
        task_text.draw()
        timer_text.draw()
        win.flip()
        
        # Check for keypresses
        keys = event.getKeys(keyList=['right', 'escape'])
        
        # Check for escape key
        if 'escape' in keys:
            win.close()
            core.quit()
            
        # Count right arrow presses
        if 'right' in keys:
            right_clicks += 1
        
        # Brief wait to prevent CPU hogging
        core.wait(0.001)
    
    # Phase 2: LEFT arrow key (if time remains and right clicks completed)
    if right_clicks >= clicks_per_side:
        while core.getTime() < end_time and left_clicks < clicks_per_side:
            # Create VERTICAL progress bar (shorter)
            progress_bar_back = visual.Rect(
                win,
                width=0.1,
                height=0.6,  # Shortened from 0.8
                fillColor='darkgrey',
                lineColor='white',
                pos=(0, 0)
            )
            
            progress_bar_fill = visual.Rect(
                win,
                width=0.1,
                height=0.6 * (left_clicks / clicks_per_side),
                fillColor='blue',
                lineColor=None,
                pos=(0, -0.3 + (0.6 * (left_clicks / clicks_per_side) / 2)),
                anchor='center'
            )
            
            # Create instruction text
            instruction_text = visual.TextStim(
                win,
                text=f"Practice trial {trial_num}\n(hard task)",
                pos=(0, 0.4),
                height=0.05,
                color='white'
            )
            
            progress_text = visual.TextStim(
                win,
                text=f"{int((left_clicks / clicks_per_side) * 100)}%",
                pos=(0.15, 0),
                height=0.05,
                color='white'
            )
            
            task_text = visual.TextStim(
                win,
                text=f"Press the LEFT arrow key with your {non_dominant_hand} pinky finger",
                pos=(0, -0.4),
                height=0.05,
                color='white'
            )
            
            # Create timer text (bottom right corner)
            time_remaining = max(0, end_time - core.getTime())
            timer_text = visual.TextStim(
                win,
                text=f"{time_remaining:.1f}s",
                pos=(0.8, -0.8),
                height=0.04,
                color='white'
            )
            
            # Draw elements
            instruction_text.draw()
            progress_bar_back.draw()
            progress_bar_fill.draw()
            progress_text.draw()
            task_text.draw()
            timer_text.draw()
            win.flip()
            
            # Check for keypresses
            keys = event.getKeys(keyList=['left', 'escape'])
            
            # Check for escape key
            if 'escape' in keys:
                win.close()
                core.quit()
                
            # Count left arrow presses
            if 'left' in keys:
                left_clicks += 1
            
            # Brief wait to prevent CPU hogging
            core.wait(0.001)
    
    # Calculate total clicks executed
    total_clicks = right_clicks + left_clicks
    
    # Check if task was completed
    task_complete = (right_clicks >= clicks_per_side and left_clicks >= clicks_per_side)
    
    return task_complete, total_clicks
