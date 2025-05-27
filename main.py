"""
main.py
Entry point for the effort-based decision task experiment.
"""

import os
from psychopy import visual, core, event, logging
import config
from utils import setup_logging, save_data
from subject_info import get_subject_info
import calibration
import instructions
import practice_trials
#import real_trials

def main():
    """
    Main experimental function that runs through all experimental stages.
    
    Executes the experiment in sequence:
    - Setup logging
    - Collect subject information
    - Initialize window
    - Run calibration
    - Run practice trials (if selected)
    - Run main experimental trials
    - Save data and clean up
    
    Returns:
    None
    """
    # Setup logging
    setup_logging()
    logging.data('Starting experiment')
    
    # Collect subject info
    info = get_subject_info()
    logging.exp(f"Subject info: {info}")
    
    # Initialize window 
    win = visual.Window(
        fullscr=True,
        color='black',     
        units='height',      
        allowGUI=True        
    )
    
    # Add text indicating exit options
    exit_instructions = visual.TextStim(
        win, 
        text="To exit: Press Cmd+Q (macOS) or Alt+F4 (Windows) or ESC key",
        pos=(0, -0.45),      # Position at bottom of screen
        height=0.025,        # Smaller text
        color='grey'         # Less prominent color
    )
    
    # Get user's handedness from info
    handedness = info['handedness'].lower()
    
    # Calibration phase
    logging.data('[STRUCTURE] Running right-hand calibration')
    
    # Show exit instructions on each screen
    exit_instructions.draw()
    
    # Run the calibration with non-dominant hand (based on handedness)
    right_count = calibration.run_calibration(win, hand='right', handedness=handedness)
    logging.data(f'[DATA] Right-key clicks: {right_count}')
    
    logging.data('[STRUCTURE] Running left-hand calibration')
    left_count = calibration.run_calibration(win, hand='left', handedness=handedness)
    logging.data(f'[DATA] Left-key clicks: {left_count}')
    
    # Compute hard click requirement (0.8 * sum of both hands)
    hard_clicks_required = int(0.8 * (right_count + left_count))
    info['hard_clicks_required'] = hard_clicks_required
    logging.data(f'[DATA] Hard clicks required: {hard_clicks_required}')
    
    # Display summary of calibration
    summary = visual.TextStim(
        win,
        text=(
            f"Calibration Complete!\n\n"
            f"Right key presses: {right_count}\n"
            f"Left key presses: {left_count}\n"
            f"Hard task will require {hard_clicks_required} presses.\n\n"
            "Press SPACE to continue."
        ),
        color='white', height=0.05, wrapWidth=1.5
    )
    summary.draw()
    exit_instructions.draw()
    win.flip()
    
    # Wait for space after calibration summary
    event.waitKeys(keyList=['space'])
    
    # Skipping during testing to go faster
#    # Run instructions
#    logging.exp('Running instructions')
#    instructions.run_instructions(win, info)
    
    # Practice trials
    all_data = []
    if info['practice_trials']:
        logging.data('[STRUCTURE] Running practice trials')
        practice_data = practice_trials.run_practice_trials(win, info)
        all_data.extend(practice_data)
        
        # After practice trials, show option to continue or repeat
        practice_end_text = visual.TextStim(
            win,
            text=(
                "End of practice trials. Please wait for the experimenter.\n\n"
                "Press SPACE to begin experiment\n"
                "Press ENTER to repeat practice trials"
            ),
            color='white', height=0.05, wrapWidth=1.5
        )
        
        # Loop until participant chooses to continue
        while True:
            practice_end_text.draw()
            win.flip()
            
            keys = event.waitKeys(keyList=['space', 'return', 'escape'])
            
            if 'escape' in keys:
                win.close()
                core.quit()
            elif 'space' in keys:
                # Continue to main experiment
                break
            elif 'return' in keys:
                # Repeat practice trials
                logging.data('[STRUCTURE] Repeating practice trials')
                practice_data = practice_trials.run_practice_trials(win, info)
                # Don't extend all_data here since we're just repeating
    else:
        logging.data('[STRUCTURE] Skipping practice trials')
    
    # Main experiment
    logging.data('[STRUCTURE] Running main experimental trials')
    #real_data = real_trials.run(win, info)
    #all_data.extend(real_data)
    # Placeholder for main trials
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Save data to /data folder
    output_path = os.path.join(data_dir, info['filename'])
    #save_data(output_path, all_data)
    logging.data(f'[STRUCTURE] Data saved to {output_path}')
    
    # Show completion message
    completion = visual.TextStim(
        win,
        text="Experiment complete.\nThank you for your participation!\n\nPress SPACE to exit.",
        color='white', height=0.05, wrapWidth=1.5
    )
    completion.draw()
    exit_instructions.draw()
    win.flip()
    
    # Wait for space key
    event.waitKeys(keyList=['space'])
    
    # Cleanup
    win.close()
    core.quit()

# Allow keyboard interrupt to exit program
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:  # Handle Ctrl+C
        core.quit()