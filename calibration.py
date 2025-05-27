"""
calibration.py
Module to calibrate hand presses.
"""

from psychopy import visual, event, core, logging
from config import CALIBRATION_DURATION

def run_calibration(win, hand='right', handedness='right'):
    """
    Run calibration task for a given hand ('right' or 'left').
    The user should always use their non-dominant hand for the task,
    as determined by the handedness parameter.
    
    Parameters:s
    win : psychopy.visual.Window
        Window to display stimuli
    hand : str
        Which arrow key to calibrate ('right' or 'left')
    handedness : str
        User's dominant hand ('right' or 'left') 
        
    Returns:
    int
        Number of valid key presses
    """
    # Determine which arrow key to use (lowercase for key detection)
    arrow_key = hand.lower()
    
    # Determine which physical hand to use (the non-dominant one)
    # If user is right-handed, they should use left hand, and vice versa
    dominant_hand = handedness.upper()
    if dominant_hand == "RIGHT":
        physical_hand = "LEFT"
    else:
        physical_hand = "RIGHT"
    
    # Add exit instruction text
    exit_instructions = visual.TextStim(
        win, 
        text="To exit: Press Cmd+Q (macOS) or Alt+F4 (Windows) or ESC key",
        pos=(0, -0.45),      # Position at bottom of screen
        height=0.025,        # Smaller text
        color='grey'         # Less prominent color
    )
    
    # Intro screen with non-dominant hand instruction
    instr = (f"Get ready to press the {arrow_key.upper()} arrow key with your NON-DOMINANT ({physical_hand}) pinky.\n\n"
             f"Press SPACE to begin.")
    
    text_stim = visual.TextStim(win, text=instr, color='white', height=0.05, wrapWidth=1.5)
    text_stim.draw()
    exit_instructions.draw()
    win.flip()
    
    # Wait for space press
    event.clearEvents()
    logging.data(f"[STRUCTURE] Starting calibration for {arrow_key} key using {physical_hand} hand")
    event.waitKeys(keyList=['space'])
    
    # 3–2–1–GO countdown
    for cnt in [3, 2, 1]:
        text_stim.text = str(cnt)
        text_stim.draw()
        exit_instructions.draw()
        win.flip()
        core.wait(1)
    
    text_stim.text = "GO!"
    text_stim.draw()
    exit_instructions.draw()
    win.flip()
    core.wait(0.5)
    
    # Prepare counter & timer texts
    count = 0
    count_text = visual.TextStim(win, text="Count: 0", color='white', pos=(0, 0.2), height=0.08)
    timer_text = visual.TextStim(win, text="", color='white', pos=(0, -0.2), height=0.06)
    
    # Clear all keyboard events before starting
    event.clearEvents()
    
    # Track key state (to prevent holding)
    key_is_down = False
    
    # Calibration loop
    start_time = core.getTime()
    end_time = start_time + CALIBRATION_DURATION
    logging.data(f"[STRUCTURE] Calibration started - Duration: {CALIBRATION_DURATION}s")
    
    while core.getTime() < end_time:
        # Get current time
        current_time = core.getTime()
        
        # Check for key presses (use lowercase arrow_key for key detection)
        keys = event.getKeys(keyList=[arrow_key])
        
        # If key is pressed and wasn't already down
        if keys and not key_is_down:
            count += 1
            key_is_down = True
            # logging.data(f"[DATA] Key press: {arrow_key} - count now: {count}")
        
        # If no keys are pressed, reset key_is_down
        if not keys:
            key_is_down = False
        
        # Update display
        count_text.text = f"Count: {count}"
        remaining = max(0, end_time - current_time)
        timer_text.text = f"Time: {remaining:.1f}s"
        
        # Draw & flip every frame
        count_text.draw()
        timer_text.draw()
        exit_instructions.draw()
        win.flip()
        
        # Add a very brief wait to prevent excessive CPU usage
        core.wait(0.001)
    
    # Log final count
    logging.data(f"[STRUCTURE] Calibration completed - Final count: {count}")
    
    # Add a short pause after calibration
    text_stim.text = f"Calibration complete: {count} presses\n\nPress SPACE to continue."
    text_stim.draw()
    exit_instructions.draw()
    win.flip()
    
    # Wait for space press
    event.clearEvents()
    event.waitKeys(keyList=['space'])
    
    return count