"""
instructions.py
Module for displaying task instructions to participants.
"""
from psychopy import visual, event, core, logging
from config import (
    ENDOWMENT_MONEY, ENDOWMENT_FOOD, INCOMPLETE_TASK_PENALTY,
    LOSS_EASY_VALUE, LOSS_HARD_VALUE, GAIN_EASY_VALUE, GAIN_HARD_VALUE,
    EASY_TASK_DURATION, HARD_TASK_DURATION,
    EXAMPLE_LOW_PROB, EXAMPLE_HIGH_PROB
)
def run_instructions(win, info, calibration_data=None):
    """
    Display comprehensive task instructions to participants.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    info : dict
        Subject information including domain, valence, and handedness
    calibration_data : dict, optional
        Contains calibration_presses_left and calibration_presses_right
        
    Returns:
    None
    """
    # Extract relevant information
    domain = info['domain']
    valence = info['valence']
    handedness = info['handedness']
    
    if 'hard_clicks_required' in info:
        hard_clicks_required = info['hard_clicks_required']
        
    if 'easy_clicks_required' in info:
        easy_clicks_required = info['easy_clicks_required']
    
    # Determine text variations based on domain and valence
    if domain == 'Money':
        unit = '$'
        unit_plural = 'dollars'
        endowment = ENDOWMENT_MONEY
        endowment_text = f'an ${endowment} endowment'
        incomplete_penalty = f'${INCOMPLETE_TASK_PENALTY:.2f}'
    else:  # Food
        unit = ''
        unit_plural = 'snacks'
        endowment = ENDOWMENT_FOOD
        endowment_text = f'{endowment} snacks'
        incomplete_penalty = f'{int(INCOMPLETE_TASK_PENALTY)} snacks'
    
    # Set values based on valence
    if valence == 'Loss':
        easy_value = LOSS_EASY_VALUE
        hard_value = LOSS_HARD_VALUE
        action_word = 'lose'
        outcome_word = 'loss'
        prob_label = 'Probability of loss:'
    else:  # Gain
        easy_value = GAIN_EASY_VALUE
        hard_value = GAIN_HARD_VALUE
        action_word = 'win'
        outcome_word = 'gain'
        prob_label = 'Probability of gain:'
    
    # Format values for display
    if domain == 'Money':
        easy_display = f"{'-' if valence == 'Loss' else '+'}{unit}{easy_value:.2f}"
        hard_display = f"{'-' if valence == 'Loss' else '+'}{unit}{hard_value:.2f}"
    else:  # Food
        easy_display = f"{'-' if valence == 'Loss' else '+'}{int(easy_value)}"
        hard_display = f"{'-' if valence == 'Loss' else '+'}{int(hard_value)}"
    
    # Determine hands
    dominant_hand = handedness.upper()
    non_dominant_hand = "LEFT" if dominant_hand == "RIGHT" else "RIGHT"
    
    # Create instruction screens
    instructions = []
    
    # Screen 1: Introduction
    instructions.append({
        'title': 'Instructions',
        'main_text': (f"You will start this task with {endowment_text}. On each\n"
                     f"trial, you will choose to complete an easy task or a hard task.\n"
                     f"The screen will look like this:"),
        'show_choice_demo': True,
        'demo_easy_value': easy_display,
        'demo_hard_value': hard_display,
        'demo_prob_label': prob_label,
        'bottom_text': "Use the left arrow key to select the easy task.\nUse the right arrow key to select the hard task.\n\nPress spacebar to continue"
    })
    
    # Screen 2: Easy task outcome
    if valence == 'Loss':
        if domain == 'Money':
            outcome_text = f"If you select the EASY task, you will have a chance of losing\n{unit}{easy_value:.2f} {unit_plural} even if you complete the task"
        else: # Food
            outcome_text = f"If you select the EASY task, you will have a chance of losing\n{int(easy_value)} {unit_plural} even if you complete the task"
    else: # Gain
        outcome_text = f"If you select the EASY task, you will have a chance of winning\n{easy_display} if you complete the task"
        
    instructions.append({
        'main_text': outcome_text,
        'show_choice_demo': True,
        'demo_easy_value': easy_display,
        'demo_hard_value': hard_display,
        'highlight_easy': True,
        'bottom_text': "Press spacebar to continue"
    })
    
    # Screen 3: Hard task outcome
    if valence == 'Loss':
        if domain == 'Money':
            outcome_text = f"If you select the HARD task, you will have a chance of losing\n{unit}{hard_value:.2f} {unit_plural} even if you complete the task"
        else:
            outcome_text = f"If you select the HARD task, you will have a chance of losing\n{int(hard_value)} {unit_plural} even if you complete the task"
    else:
        outcome_text = f"If you select the HARD task, you will have a chance of winning\n{hard_display} if you complete the task"
        
    instructions.append({
        'main_text': outcome_text,
        'show_choice_demo': True,
        'demo_easy_value': easy_display,
        'demo_hard_value': hard_display,
        'highlight_hard': True,
        'bottom_text': "Press spacebar to continue"
    })
    
    # Screen 4: Easy task details
    instructions.append({
        'main_text': (f"The EASY task requires you to press the SPACE BAR {easy_clicks_required}\n"
                     f"times in {int(EASY_TASK_DURATION)} seconds using the index finger of your {dominant_hand} hand"),
        'show_progress_demo': True,
        'progress_text': "A shaded bar will indicate your progress as you complete\nthe task:",
        'bottom_text': "Press spacebar to continue"
    })
    
    # Screen 5: Hard task details
    instructions.append({
        'main_text': (f"The HARD task requires you to press the RIGHT ARROW KEY\n"
                     f"{hard_clicks_required} times and the LEFT ARROW KEY {hard_clicks_required} times in {int(HARD_TASK_DURATION)} seconds\n"
                     f"using the pinky finger of your {non_dominant_hand} hand"),
        'show_progress_demo': True,
        'progress_text': "A shaded bar will indicate your progress as you complete\nthe task:",
        'bottom_text': "Press spacebar to continue"
    })
    
    # Screen 6: Probability explanation - low
    if valence == 'Loss':
        prob_text = (f"On each trial, there is a CHANCE that you will {action_word} the\n"
                    f"amount of {unit_plural} shown on the screen even if you\n"
                    f"complete the task in the allotted time")
    else:
        prob_text = (f"On each trial, there is a CHANCE that you will {action_word} the\n"
                    f"amount of {unit_plural} shown on the screen if you\n"
                    f"complete the task in the allotted time")
    
    instructions.append({
        'main_text': prob_text,
        'show_choice_demo': True,
        'demo_probability': EXAMPLE_LOW_PROB,
        'demo_prob_label': prob_label,
        'demo_easy_value': easy_display,
        'demo_hard_value': easy_display,  # Both show easy value as per PDF
        'bottom_text': "Press spacebar to continue"
    })
    
    # Screen 7: Probability explanation - high
    if valence == 'Loss':
        high_prob_text = (f"If a higher probability is shown, you are MORE LIKELY TO\n"
                         f"LOSE {unit_plural.upper()} even if you complete the task")
    else:
        high_prob_text = (f"If a higher probability is shown, you are MORE LIKELY TO\n"
                         f"WIN {unit_plural.upper()} if you complete the task")
    
    instructions.append({
        'main_text': high_prob_text,
        'show_choice_demo': True,
        'demo_probability': EXAMPLE_HIGH_PROB,
        'demo_prob_label': prob_label,
        'demo_easy_value': easy_display,
        'demo_hard_value': hard_display,
        'bottom_text': "Press spacebar to continue"
    })
    
    # Screen 8: Incomplete task penalty
    if valence == 'Loss':
        penalty_text = f"If you do NOT complete the task, you will always (100%)\nlose {incomplete_penalty}"
    else:
        if domain == 'Money':
            penalty_text = f"If you do NOT complete the task, you will always (100%)\nwin $0"
        else:
            penalty_text = f"If you do NOT complete the task, you will always (100%)\nwin 0 snacks"
    
    instructions.append({
        'main_text': penalty_text,
        'bottom_text': "Press spacebar to continue"
    })
    
    # Screen 9: Multiple choices
    instructions.append({
        'main_text': "You will make several choices between different options\nover the course of this experiment.",
        'bottom_text': "Press spacebar to continue"
    })
    
    # Screen 10: Payment/reward information
    if domain == 'Money':
        if valence == 'Loss':
            payment_text = (f"At the end of the task, ONE of the trials you played will be\n"
                          f"randomly selected and deducted from your ${endowment}\n"
                          f"endowment. Any endowment remaining after this\n"
                          f"deduction will be added to your participation fee as a\n"
                          f"bonus.\n\n"
                          f"In other words, your performance on this task determines\n"
                          f"how much MORE you can take home in addition to your\n"
                          f"participation fee.")
        else:  # Gain
            payment_text = (f"At the end of the task, ONE of the trials you played will be\n"
                          f"randomly selected and added to your participation fee as a bonus.\n\n"
                          f"In other words, your performance on this task determines\n"
                          f"how much MORE you can take home in addition to your\n"
                          f"participation fee.")
    else:  # Food
        if valence == 'Loss':
            payment_text = (f"At the end of the task, ONE of the trials you played will be\n"
                          f"randomly selected and deducted from your {endowment} snack\n"
                          f"endowment. Any snacks remaining after this\n"
                          f"deduction will be yours to take home.\n\n"
                          f"In other words, your performance on this task determines\n"
                          f"how many snacks you can take home.")
        else:  # Gain
            payment_text = (f"At the end of the task, ONE of the trials you played will be\n"
                          f"randomly selected and you will receive that many snacks.\n\n"
                          f"In other words, your performance on this task determines\n"
                          f"how many snacks you can take home.")
    
    instructions.append({
        'main_text': payment_text,
        'bottom_text': "Press enter to begin",
        'wait_key': 'return'
    })
    
    # Display each instruction screen
    for i, instruction in enumerate(instructions):
        display_instruction_screen(win, instruction)

def display_instruction_screen(win, instruction):
    """
    Display a single instruction screen with improved formatting.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    instruction : dict
        Dictionary containing instruction screen specifications
    """
    # Create list to hold all visual elements
    elements = []
    
    # Title if present
    if 'title' in instruction:
        title = visual.TextStim(
            win,
            text=instruction['title'],
            pos=(0, 0.4),
            height=0.06,
            color='white',
            bold=True
        )
        elements.append(title)
    
    # Main text
    main_text = visual.TextStim(
        win,
        text=instruction['main_text'],
        pos=(0, 0.2),
        height=0.04,
        color='white',
        wrapWidth=1.8,
        alignText='center'
    )
    elements.append(main_text)
    
    # Choice demonstration if needed
    if instruction.get('show_choice_demo'):
        # Gray background box
        choice_bg = visual.Rect(
            win,
            width=1.25, 
            height=0.4,
            fillColor=[0.2, 0.2, 0.2],
            pos=(0, -0.1)
        )
        elements.append(choice_bg)
        
        # "Please choose a task:" header
        choice_header = visual.TextStim(
            win,
            text="Please choose a task:",
            pos=(0, 0.05),
            height=0.035,
            color='white'
        )
        elements.append(choice_header)
        
        # Easy option box
        easy_box = visual.Rect(
            win,
            width=0.35,
            height=0.18,
            fillColor=[0.6, 0.6, 0.6],
            lineColor='red' if instruction.get('highlight_easy') else 'white',
            lineWidth=3 if instruction.get('highlight_easy') else 1,
            pos=(-0.35, -0.15)  # Moved down from -0.1 to -0.15
        )
        elements.append(easy_box)
        
        easy_label = visual.TextStim(
            win,
            text="Easy",
            pos=(-0.35, -0.10),  # Moved down from -0.05 to -0.10
            height=0.035,
            color='black',
            bold=True
        )
        elements.append(easy_label)
        
        easy_value = visual.TextStim(
            win,
            text=instruction['demo_easy_value'],
            pos=(-0.35, -0.20),  # Moved down from -0.15 to -0.20
            height=0.04,
            color='black'
        )
        elements.append(easy_value)
        
        easy_key = visual.TextStim(
            win,
            text="(left arrow key)",
            pos=(-0.35, -0.28),  # Moved down from -0.23 to -0.28
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
            lineColor='red' if instruction.get('highlight_hard') else 'white',
            lineWidth=3 if instruction.get('highlight_hard') else 1,
            pos=(0.35, -0.15)  # Already at -0.15
        )
        elements.append(hard_box)
        
        hard_label = visual.TextStim(
            win,
            text="Hard",
            pos=(0.35, -0.10),  # Moved down from -0.05 to -0.10
            height=0.035,
            color='black',
            bold=True
        )
        elements.append(hard_label)
        
        hard_value = visual.TextStim(
            win,
            text=instruction['demo_hard_value'],
            pos=(0.35, -0.20),  # Moved down from -0.1 to -0.20
            height=0.04,
            color='black'
        )
        elements.append(hard_value)
        
        hard_key = visual.TextStim(
            win,
            text="(right arrow key)",
            pos=(0.35, -0.28),  # Moved down from -0.23 to -0.28
            height=0.025,
            color='white'
        )
        elements.append(hard_key)
        
        # Probability display if needed
        if 'demo_probability' in instruction:
            prob_text = visual.TextStim(
                win,
                text=f"{instruction['demo_prob_label']} {instruction['demo_probability']}%",
                pos=(0, -0.01),
                height=0.035,
                color='white'
            )
            elements.append(prob_text)
    
    # Progress bar demonstration if needed
    if instruction.get('show_progress_demo'):
        if 'progress_text' in instruction:
            progress_label = visual.TextStim(
                win,
                text=instruction['progress_text'],
                pos=(0, 0.05), # was 0.1
                height=0.035,  
                color='white'
            )
            elements.append(progress_label)
        
        # Progress bar background -> smaller vertical bar like in practice trials
        progress_bg = visual.Rect(
            win,
            width=0.1,
            height=0.35,  
            fillColor='darkgrey',  
            lineColor='white',
            pos=(0, -0.2)  
        )
        elements.append(progress_bg)
        
        # Progress bar fill, (37%) just as an example
        progress = 0.37
        bar_height = 0.35 
        new_height = bar_height * progress
        progress_fill = visual.Rect(
            win,
            width=0.1,
            height=new_height,
            fillColor='blue',  # Match practice trials
            lineColor=None,
            pos=(0, -0.2 - (bar_height - new_height) / 2)  
        )
        elements.append(progress_fill)
        
        # Percentage text - positioned like in practice trials
        percent_text = visual.TextStim(
            win,
            text="37%",
            pos=(0.15, -0.2),  # Aligned with center of progress bar
            height=0.035,
            color='white',
            bold=True
        )
        elements.append(percent_text)
    
    # Bottom instruction text
    bottom_text = visual.TextStim(
        win,
        text=instruction['bottom_text'],
        pos=(0, -0.4),
        height=0.035,
        color='yellow',
        wrapWidth=1.8,
        alignText='center'
    )
    elements.append(bottom_text)
    
    # Draw all elements
    for element in elements:
        element.draw()
    
    win.flip()
    
    # Wait for keypress
    wait_key = instruction.get('wait_key', 'space')
    keys = event.waitKeys(keyList=[wait_key, 'escape'])
    
    if 'escape' in keys:
        logging.info('User pressed escape during instructions')
        win.close()
        core.quit()