"""
Utility functions for StudentHub
"""

from datetime import datetime
import json


def format_date(date_string):
    """Convert date string to datetime object"""
    # TODO: Add error handling for invalid date formats
    return datetime.strptime(date_string, "%Y-%m-%d")


def calculate_days_remaining(deadline):
    """Calculate days remaining until deadline"""
    today = datetime.now()
    delta = deadline - today
    return delta.days


def validate_grade(grade):
    """Validate if grade is between 0 and 100"""
    if grade < 0 or grade > 100:
        return False
    return True


def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_from_json(filename):
    """Load data from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_priority_level(days_remaining):
    """Determine priority based on days remaining
    working on this issue for the first time
    fix
    """
    if days_remaining < 0:
        return "OVERDUE"
    elif days_remaining <= 3:
        return "HIGH"
    elif days_remaining <= 7:
        return "MEDIUM"
    else:
        return "LOW"
