"""
Utility functions for StudentHub
"""

from datetime import datetime
import json
import csv


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
    """Determine priority based on days remaining"""
    if days_remaining < 0:
        return "OVERDUE"
    elif days_remaining <= 3:
        return "HIGH"
    elif days_remaining <= 7:
        return "MEDIUM"
    else:
        return "LOW"

def export_to_csv(data, filename, headers=None):
    """Export list of dicts to CSV"""
    if not data:
        raise ValueError("No data to export")

    if headers is None:
        headers = list(data[0].keys())

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)