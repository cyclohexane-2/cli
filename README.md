StudentHub - Learning Management CLI Tool

A simple command-line tool to help students manage their assignments, track deadlines, and organize study sessions.

Perfect for learning open source contributions! This project has beginner-friendly issues ready for you to solve.
Quick Start

👉 New to this project? Read QUICKSTART.md for a 5-minute setup guide!
Features

    Add and track assignments
    Set deadlines and get reminders
    Calculate grade averages
    Organize study sessions with a Pomodoro timer
    Export data to JSON

Installation

# Navigate to the project directory
cd demo

# No external dependencies needed for basic functionality!
# (Optional) Install testing dependencies
pip install pytest

Usage Examples
Basic Commands

# See all available commands
python main.py --help

# Add an assignment
python main.py add-assignment "Math Homework" --deadline "2025-12-01" --subject "Mathematics."

# List all pending assignments
python main.py list

# Mark assignment as completed
python main.py complete "Math Homework."

# Calculate your GPA
python main.py gpa

# View statistics
python main.py stats

# Start the Pomodoro
python main.py pomodoro

# Start a Pomodoro run non-interactively (4 sessions, 25/5 by default)
python main.py pomodoro --sessions 4

# Custom Pomodoro durations
python main.py pomodoro --sessions 3 --work 30 --break-minutes 10

# Mute Pomodoro sounds/notifications
python main.py pomodoro --no-sound

Example Session

$ python main.py add-assignment "Physics Lab" --deadline "2025-11-30" --subject "Physics"
Added assignment: Physics Lab

$ python main.py add-assignment "History Essay" --deadline "2025-12-05" --subject "History"
Added assignment: History Essay

$ python main.py stats
=== Your Statistics ===
Total Assignments: 2
Completed: 0
Pending: 2
GPA: 0.00

# Example Pomodoro usage (interactive)
$ python main.py pomodoro
<ASCII splash appears, choose options to Start/Configure/Quick test/Quit>

# Example Pomodoro non-interactive quick test
$ python main.py pomodoro --sessions 1 --work 0.1 --break-minutes 0.1
(Start runs with very short work/break for quick verification)

Running Tests

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m unittest tests/test_utils.py

Project Structure

demo/
├── main.py              # Entry point
├── utils.py             # Utility functions
├── student_manager.py   # Core functionality
├── pomodoro.py          # Pomodoro timer module (interactive menu + countdown)
├── tests/               # Test files
├── README.md            # This file
├── CONTRIBUTING.md      # Contribution guidelines
└── ISSUES.md            # List of open issues for contributors

Contributing

We welcome contributions from everyone! This project is specifically designed for learning.
Getting Started with Contributing

    First time? Read QUICKSTART.md for a 5-minute guide
    Ready to contribute? Check CONTRIBUTING.md for detailed guidelines
    Pick an issue: Browse ISSUES.md for beginner-friendly tasks

Available Issues by Difficulty

    Beginner (Good First Issues): #1, #2, #3, #4
    Intermediate: #5, #6, #7
    Advanced: #8, #9, #10

Start with Issue #2 if you're brand new to open source - it takes less than 1 minute!
Workshop/Session Guide

If you're an instructor using this for teaching:

    Setup (5 min): Students clone repo and run python main.py --help
    Demo (10 min): Show how to fix Issue #2 end-to-end
    Practice (45+ min): Students pick and solve issues
    Review (15 min): Discuss solutions and best practices

All issues include:

    Clear descriptions
    Expected outcomes
    Skills students will learn
    Difficulty ratings

License
MIT License
