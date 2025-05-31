"""
main.py
Entry point for the effort-based decision task experiment.
"""
import os
import sys
from psychopy import visual, core, event, logging
import config
from utils import setup_logging, save_data, save_partial_data
from subject_info import get_subject_info
import calibration
import instructions
import practice_trials
from real_trials import run_real_trials

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
    # Initialize variables for cleanup
    win = None
    info = None
    all_data = []
    
    try:
        # Collect subject info FIRST
        info = get_subject_info()
        
        # Setup logging with subject info for matching filename
        setup_logging(info)
        logging.data('Starting experiment')
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
        
        # 5/28 Meeting: Compute easy click requirement (0.20 * max clicks from hard calibration)
        max_calibration_clicks = max(left_count, right_count)
        easy_clicks_required = int(0.2 * max_calibration_clicks)
        info['easy_clicks_required'] = easy_clicks_required
        logging.data(f'[DATA] Easy clicks required: {easy_clicks_required}')
        
        # Display summary of calibration
        summary = visual.TextStim(
            win,
            text=(
                f"Calibration Complete!\n\n"
                f"Right key presses: {right_count}\n"
                f"Left key presses: {left_count}\n"
                f"Easy task will require {easy_clicks_required} presses.\n"
                f"Hard task will require {hard_clicks_required} presses.\n\n"
                "Press SPACE to continue."
            ),
            color='white', height=0.05, wrapWidth=1.5
        )
        summary.draw()
        exit_instructions.draw()
        win.flip()
        
        # Wait for space after calibration summary
        keys = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            raise KeyboardInterrupt("User pressed escape")
        
        # Skipping instructions during testing for speed...
        # Run instructions (uncomment when ready)
        logging.data('[STRUCTURE] Running instructions')
        instructions.run_instructions(win, info)
        
        # Practice trials
        if info['practice_trials']:
            logging.data('[STRUCTURE] Running practice trials')
            try:
                practice_data = practice_trials.run_practice_trials(win, info)
                all_data.extend(practice_data)
            except Exception as e:
                logging.error(f"Error during practice trials: {e}")
                save_partial_data(info, all_data, "Error during practice trials")
                raise
            
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
                    raise KeyboardInterrupt("User pressed escape after practice")
                elif 'space' in keys:
                    # Continue to main experiment
                    break
                elif 'return' in keys:
                    # Repeat practice trials
                    logging.data('[STRUCTURE] Repeating practice trials')
                    try:
                        practice_data = practice_trials.run_practice_trials(win, info)
                        # Don't extend all_data here since we're just repeating
                    except Exception as e:
                        logging.error(f"Error during practice trial repeat: {e}")
                        save_partial_data(info, all_data, "Error during practice trial repeat")
                        raise
        else:
            logging.data('[STRUCTURE] Skipping practice trials')
        
        # Main experiment
        logging.data('[STRUCTURE] Running main experimental trials')
        try:
            real_data = run_real_trials(win, info)
            all_data.extend(real_data)
        except Exception as e:
            logging.error(f"Error during main experiment: {e}")
            save_partial_data(info, all_data, "Error during main experiment")
            raise
        
        # If we get here, experiment completed normally
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Save complete data to /data folder
        output_path = os.path.join(data_dir, info['filename'])
        save_data(output_path, all_data)
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
        
    except KeyboardInterrupt as e:
        # User pressed escape or Ctrl+C
        logging.data(f"Experiment terminated by user: {e}")
        if info:
            save_partial_data(info, all_data, "User terminated (ESC/Ctrl+C)")
        
    except Exception as e:
        # Any other error
        logging.error(f"Unexpected error: {e}")
        if info:
            save_partial_data(info, all_data, f"Unexpected error: {str(e)}")
        raise
        
    finally:
        # Cleanup 
        if win:
            win.close()
        core.quit()

# Allow keyboard interrupt to exit program
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Final catch-all
        print(f"Fatal error: {e}")
        sys.exit(1)