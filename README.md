# Effort-Based Decision Making Task

A PsychoPy experiment examining how participants choose between low-effort and high-effort tasks for varying rewards across different domains (money/food) and valences (gains/losses).

## Quick Start

**Requirements:** PsychoPy (any recent version)

1. Open `main.py` in PsychoPy
2. Run the experiment (Cmd+R)
3. Follow GUI prompts for participant info
4. Experiment runs automatically through calibration → instructions → trials (Cmd+Q to quit at any point)

## Task Overview

Participants choose between:
- **Easy Task**: Press spacebar with dominant hand (7 seconds)
- **Hard Task**: Press arrow keys with non-dominant hand (21 seconds)

**Experimental factors:**
- **Domain**: Money ($) vs Food (snacks)
- **Valence**: Gains (earning) vs Losses (losing from endowment)
- **Magnitude**: Variable reward amounts
- **Probability**: 12%, 50%, or 88% chance of outcome

## Data Output

- **Trial data**: `data/[SubjectID]_[Domain]_[Valence]_[OptionalVersion].csv`
- **Logs**: `logs/[SubjectID]_[Domain]_[Valence]_[OptionalVersion].log`

Key measures: choice, reaction time, task completion, reward magnitude, probability

## Code Structure

```
main.py              # Experiment orchestration
subject_info.py      # Participant information GUI
calibration.py       # Effort calibration
instructions.py      # Task instructions
practice_trials.py   # Practice trials
real_trials.py       # Main experiment
config.py            # Parameters
utils.py             # Data utilities
```
