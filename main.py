"""
main.py
Entry point for the effort-based decision task experiment.
"""
import os
import sys
from psychopy import visual, core, event, logging
from config import N_REAL_TRIALS_MONEY, N_REAL_TRIALS_FOOD, N_CATCH_TRIALS
from utils import setup_logging, create_data_file, count_trials_in_file
from subject_info import get_subject_info
import calibration
import instructions
import practice_trials
from real_trials import run_real_trials

def show_phase_transition(win, phase_name, duration=1.5):
    """
    Display a phase transition screen.
    
    Parameters:
    win : psychopy.visual.Window
        Window to display stimuli
    phase_name : str
        Name of the phase being entered
    duration : float
        How long to display the screen (seconds)
    """

    # Add grey background
    phase_bg = visual.Rect(
        win,
        width=2.0,
        height=2.0,
        fillColor=[0.2, 0.2, 0.2],
        pos=(0, 0)
    )

    # Create phase transition text
    phase_text = visual.TextStim(
        win,
        text=f"Entering {phase_name} Phase",
        height=0.06,
        color='white',
        bold=True
    )
    
    # Add exit instruction text (consistent with other screens)
    exit_instructions = visual.TextStim(
        win, 
        text="To exit: Press the ESC key",
        pos=(0, -0.45),
        height=0.025,
        color=[0.7, 0.7, 0.7]
    )
    
    # Draw and display
    phase_bg.draw()
    phase_text.draw()
    exit_instructions.draw()
    win.flip()
    
    # Wait for specified duration
    core.wait(duration)

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
    - Check completion and rename if partial
    
    Returns:
    None
    """
    try:
        # Collect subject info FIRST
        info = get_subject_info()
        
        # Setup logging with subject info for matching filename
        setup_logging(info)
        logging.data('Starting experiment')
        logging.exp(f"Subject info: {info}")
        
        # Create data file immediately
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        data_file_path = os.path.join(data_dir, info['filename'])
        info['data_file_path'] = data_file_path

        # Create empty CSV with headers
        create_data_file(data_file_path)
        
        # Initialize window 
        win = visual.Window(
            fullscr=True,
            color=[0.2, 0.2, 0.2],  # change to grey
            units='height',      
            allowGUI=True        
        )
        
        # Add text indicating exit options
        exit_instructions = visual.TextStim(
            win, 
            text="To exit: Press the ESC key",
            pos=(0, -0.45),      # Position at bottom of screen
            height=0.025,        # Smaller text
            color=[0.7, 0.7, 0.7]
        )
        
        # Get user's handedness from info
        handedness = info['handedness'].lower()
        
        # Calibration phase
        show_phase_transition(win, "Calibration")  
        logging.data('[STRUCTURE] Running right-hand calibration')
        
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
        
        # Compute easy click requirement (0.20 * max clicks from hard calibration)
        max_calibration_clicks = max(left_count, right_count)
        easy_clicks_required = int(0.2 * max_calibration_clicks)
        info['easy_clicks_required'] = easy_clicks_required
        logging.data(f'[DATA] Easy clicks required: {easy_clicks_required}')
        
        # Display summary of calibration
        # Add grey background
        summary_bg = visual.Rect(
            win,
            width=2.0,
            height=2.0,
            fillColor=[0.2, 0.2, 0.2],
            pos=(0, 0)
        )

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
        summary_bg.draw()
        summary.draw()
        exit_instructions.draw()
        win.flip()
        
        # Wait for space after calibration summary
        keys = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            logging.data("User pressed escape during calibration summary")
            win.close()
            core.quit()
            return
        
        # Run instructions
        show_phase_transition(win, "Instructions") 
        logging.data('[STRUCTURE] Running instructions')
        instructions.run_instructions(win, info)
        
        # Practice trials
        practice_rounds_completed = 0
        if info['practice_trials']:
            while True:  # Loop for repeated practice trials
                practice_rounds_completed += 1
                show_phase_transition(win, f"Practice Trials (Round {practice_rounds_completed})")
                logging.data(f'[STRUCTURE] Running practice trials - Round {practice_rounds_completed}')
                practice_trials.run_practice_trials(win, info)
                
                # After practice trials, show option to continue or repeat
                # Add grey background
                practice_end_bg = visual.Rect(
                    win,
                    width=2.0,
                    height=2.0,
                    fillColor=[0.2, 0.2, 0.2],
                    pos=(0, 0)
                )

                practice_end_text = visual.TextStim(
                    win,
                    text=(
                        f"End of practice trials (Round {practice_rounds_completed}). Please wait for the experimenter.\n\n"
                        "Press SPACE to begin experiment\n"
                        "Press ENTER to repeat practice trials"
                    ),
                    color='white', height=0.05, wrapWidth=1.5
                )
                
                # Show choice and get response
                practice_end_bg.draw() 
                practice_end_text.draw()
                win.flip()
                
                keys = event.waitKeys(keyList=['space', 'return', 'escape'])
                
                if 'escape' in keys:
                    logging.data("User pressed escape after practice")
                    win.close()
                    core.quit()
                    return
                elif 'space' in keys:
                    # Continue to main experiment
                    break
                elif 'return' in keys:
                    # Continue loop to repeat practice trials
                    logging.data('[STRUCTURE] Repeating practice trials')
                    continue
        else:
            practice_rounds_completed = 0
            logging.data('[STRUCTURE] Skipping practice trials')
        
        # Store practice rounds completed in info for CSV logging
        info['practice_rounds_completed'] = practice_rounds_completed
        
        # Log final practice count
        logging.data(f'[STRUCTURE] Practice trials completed: {practice_rounds_completed} rounds')
        
        # Main experiment
        show_phase_transition(win, "Main Experiment")  
        logging.data('[STRUCTURE] Running main experimental trials')
        try:
            run_real_trials(win, info)
            # If we reach here, experiment completed successfully
            expected_trials = (N_REAL_TRIALS_MONEY if info['domain'] == 'Money' else N_REAL_TRIALS_FOOD) + N_CATCH_TRIALS
            actual_trials = count_trials_in_file(data_file_path)
            logging.data(f'[STRUCTURE] Experiment completed successfully - {actual_trials} trials saved')
        except KeyboardInterrupt:
            # Handle early termination from real trials
            logging.data("Experiment terminated during main trials")
            expected_trials = (N_REAL_TRIALS_MONEY if info['domain'] == 'Money' else N_REAL_TRIALS_FOOD) + N_CATCH_TRIALS
            actual_trials = count_trials_in_file(data_file_path)
            
            logging.data(f"[STRUCTURE] Expected: {expected_trials}, Actual: {actual_trials}")
    
            if actual_trials < expected_trials:
                # Rename file to indicate partial completion
                partial_path = os.path.join(data_dir, f"{info['base_filename']}_PARTIAL.csv")
                os.rename(data_file_path, partial_path)
                logging.data(f"[STRUCTURE] Incomplete experiment - renamed to {partial_path}")
            
            # Re-raise to exit cleanly
            raise
        
        # Show completion message
        # Add grey background
        completion_bg = visual.Rect(
            win,
            width=2.0,
            height=2.0,
            fillColor=[0.2, 0.2, 0.2],
            pos=(0, 0)
        )

        completion = visual.TextStim(
            win,
            text="Experiment complete.\nThank you for your participation!\n\nPress SPACE to exit.",
            color='white', height=0.05, wrapWidth=1.5
        )
        completion_bg.draw()
        completion.draw()
        exit_instructions.draw()
        win.flip()
        
        # Wait for space key
        event.waitKeys(keyList=['space'])
        
        # Cleanup 
        win.close()
        core.quit()
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        logging.data("Experiment terminated by user (Ctrl+C)")
        if 'win' in locals():
            win.close()
        core.quit()
        
    except Exception as e:
        # Any other error
        logging.error(f"Unexpected error: {e}")
        if 'win' in locals():
            win.close()
        core.quit()
        raise

# Allow keyboard interrupt to exit program
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Final catch-all
        print(f"Fatal error: {e}")
        sys.exit(1)