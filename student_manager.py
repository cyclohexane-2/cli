"""
Core StudentHub functionality
"""

from datetime import datetime
from utils import calculate_days_remaining, validate_grade, get_priority_level, export_to_csv, save_to_json, load_from_json


class StudentManager:
    def __init__(self):
        self.assignments = []
        self.grades = []
        self.storage_file = "student_data.json"
        self._load_data()
    
    def _load_data(self):
        data = load_from_json(self.storage_file)
        self.assignments = data.get("assignments", [])
        self.grades = data.get("grades", [])

        from datetime import datetime
        for a in self.assignments:
            a["deadline"] = datetime.strptime(a["deadline"], "%Y-%m-%d")
            a["created_at"] = datetime.strptime(a["created_at"], "%Y-%m-%d")

        for g in self.grades:
            g["date"] = datetime.strptime(g["date"], "%Y-%m-%d")

    def _save_data(self):
        save_to_json({
            "assignments": [
                {
                    "title": a["title"],
                    "deadline": a["deadline"].strftime("%Y-%m-%d"),
                    "subject": a["subject"],
                    "completed": a["completed"],
                    "created_at": a["created_at"].strftime("%Y-%m-%d")
                }
                for a in self.assignments
            ],
            "grades": [
                {
                    "subject": g["subject"],
                    "grade": g["grade"],
                    "date": g["date"].strftime("%Y-%m-%d")
                }
                for g in self.grades
            ]
        }, self.storage_file)


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
        self._save_data()
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
                self._save_data()
                return True
        return False

    def add_grade(self, subject, grade):
        """Add a grade for a subject"""
        if not validate_grade(grade):
            raise ValueError("Grade must be between 0 and 100")

        self.grades.append({
            'subject': subject,
            'grade': grade,
            'date': datetime.now()
        })
        self._save_data()

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
    
    def export_assignments(self, filename):
        """Export assignments to CSV"""
        cleaned = []
        for a in self.assignments:
            cleaned.append({
                "title": a["title"],
                "deadline": a["deadline"].strftime("%Y-%m-%d"),
                "subject": a["subject"],
                "completed": a["completed"],
                "created_at": a["created_at"].strftime("%Y-%m-%d")
            })
        export_to_csv(cleaned, filename)

    def export_grades(self, filename):
        """Export grades to CSV"""
        cleaned = []
        for g in self.grades:
            cleaned.append({
                "subject": g["subject"],
                "grade": g["grade"],
                "date": g["date"].strftime("%Y-%m-%d")
            })
        export_to_csv(cleaned, filename)
