"""
config.py
Global configuration parameters for the effort-based decision task experiment 
"""

N_REAL_TRIALS_MONEY = 42  # 14 values × 3 probabilities
N_REAL_TRIALS_FOOD = 36   # 4 values × 3 probabilities × 3 repetitions

# Number of catch trials
N_CATCH_TRIALS = 3

# Monetary magnitudes 
MONEY_MAGNITUDES = [
    1.00, 1.23, 1.46, 1.69, 1.92,
    2.15, 2.38, 2.61, 2.84, 3.07,
    3.30, 3.53, 3.76, 3.99, 4.00
]

# Food magnitudes
FOOD_MAGNITUDES = [1, 2, 3, 4]

# Probabilities of loss
PROBABILITIES = [0.12, 0.50, 0.88]

# Inter-trial interval jitter range (in seconds) 
ITI_RANGE = (1.0, 2.0)

# Click requirements
# EASY_CLICKS_REQUIRED = 30  # for easy task --> will be subject to calibration now
EASY_TASK_DURATION = 7.0   # seconds allowed for easy task
HARD_TASK_DURATION = 21.0  # seconds allowed for hard task

# Calibration duration for each key press block (in seconds)
CALIBRATION_DURATION = 3 # TODO: should be 10.5

# Practice trials configuration (monetary only)
PRACTICE_TRIALS = [
    {'magnitude_hard': 1.00, 'prob': 0.88},
    {'magnitude_hard': 2.50, 'prob': 0.50},
    {'magnitude_hard': 3.90, 'prob': 0.12},
]

# Might be unnecessary since they are bound to happen anyway
CATCH_TRIAL_CONFIGS = {
    'Loss': {
        'easy_value': 4.00,
        'hard_value': 4.00,  # Same as easy - irrational to choose hard
        'probability': 0.50
    },
    'Gain': {
        'easy_value': 1.00,
        'hard_value': 1.00,  # Same as easy - irrational to choose hard
        'probability': 0.50
    }
}

# Task parameters shown in instructions
ENDOWMENT_MONEY = 8
ENDOWMENT_FOOD = 8
INCOMPLETE_TASK_PENALTY = 4.00

# Values for different conditions
LOSS_EASY_VALUE = 4.00
LOSS_HARD_VALUE = 2.50
GAIN_EASY_VALUE = 1.00 
GAIN_HARD_VALUE = 4.00

# Example probabilities shown in instructions
EXAMPLE_LOW_PROB = 12
EXAMPLE_HIGH_PROB = 88

# Text sizes
TITLE_HEIGHT = 0.06
MAIN_TEXT_HEIGHT = 0.04
SMALL_TEXT_HEIGHT = 0.035
TINY_TEXT_HEIGHT = 0.025

# Colors (in PsychoPy -1 to 1 format)
BACKGROUND_COLOR = 'black'
TEXT_COLOR = 'white'
INSTRUCTION_COLOR = 'yellow'
BOX_FILL_COLOR = [0.6, 0.6, 0.6]
CHOICE_BG_COLOR = [0.2, 0.2, 0.2]
HIGHLIGHT_COLOR = 'red'
PROGRESS_FILL_COLOR = 'green'

# Layout dimensions
CHOICE_BOX_WIDTH = 0.35
CHOICE_BOX_HEIGHT = 0.18
CHOICE_BOX_SEPARATION = 0.7
PROGRESS_BAR_WIDTH = 0.8
PROGRESS_BAR_HEIGHT = 0.08
