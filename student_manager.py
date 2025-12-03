"""
Core StudentHub functionality
"""

from datetime import datetime
from utils import calculate_days_remaining, validate_grade, get_priority_level


class StudentManager:
    def __init__(self):
        self.assignments = []
        self.grades = []

    def add_assignment(self, title, deadline, subject=None):
        """Add a new assignment"""
        assignment = {
            'title': title,
            'deadline': deadline,
            'subject': subject,
            'completed': False,
            'created_at': datetime.now()
        }
        self.assignments.append(assignment)
        return assignment

    def list_assignments(self, show_completed=False):
        """List all assignments"""
        if show_completed:
            return self.assignments
        return [a for a in self.assignments if not a['completed']]

    def mark_completed(self, title):
        """Mark an assignment as completed"""
        for assignment in self.assignments:
            if assignment['title'] == title:
                assignment['completed'] = True
                return True
        return False

    def add_grade(self, subject, grade):
        """To check that the grade is integer or not"""
        if not isinstance(grade, int):
            raise TypeError("Grade must be an integer")
        
        """Add a grade for a subject"""
        if not validate_grade(grade):
            raise ValueError("Grade must be between 0 and 100")

        self.grades.append({
            'subject': subject,
            'grade': grade,
            'date': datetime.now()
        })

    def calculate_gpa(self):
        """Calculate GPA from grades"""
        if not self.grades:
            return 0.0

        total = sum(g['grade'] for g in self.grades)
        return total / len(self.grades)

    def get_upcoming_deadlines(self, days=7):
        """Get assignments due within specified days"""
        upcoming = []
        for assignment in self.assignments:
            if assignment['completed']:
                continue

            days_left = calculate_days_remaining(assignment['deadline'])
            if 0 <= days_left <= days:
                upcoming.append({
                    **assignment,
                    'days_remaining': days_left,
                    'priority': get_priority_level(days_left)
                })

        return sorted(upcoming, key=lambda x: x['days_remaining'])

    def get_statistics(self):
        """Get student statistics"""
        total_assignments = len(self.assignments)
        completed = sum(1 for a in self.assignments if a['completed'])

        return {
            'total_assignments': total_assignments,
            'completed': completed,
            'pending': total_assignments - completed,
            'gpa': self.calculate_gpa()
        }
