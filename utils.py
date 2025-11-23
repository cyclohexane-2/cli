"""
Utility functions for StudentHub
"""

from datetime import datetime
import json
import os

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        """Handles special case of date serialization"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
    
class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        """Handles special case of date deserialization"""
        for key, value in obj.items():
            if isinstance(value, str):
                try:
                    obj[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass  # Not a datetime string
        return obj

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
        # NOTE: Edit DateTimeEncoder accordingly if StudentManager contains other non serialiseable types
        json.dump(data, f, indent=4, cls=DateTimeEncoder)

def load_from_json(filename):
    """Load data from JSON file"""
    try:
        with open(filename, 'r') as f:
            # NOTE: Edit DateTimeDecoder accordingly if StudentManager contains other non serialiseable types
            return json.load(f, cls=DateTimeDecoder)
    except FileNotFoundError:
        return {
            "status": 1
        }
    except json.JSONDecodeError as e:
        os.remove(filename)
        return {
            "status": 2
        }


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
