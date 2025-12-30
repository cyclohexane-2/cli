import pytest
from datetime import datetime, timedelta
from student_manager import StudentManager


@pytest.fixture
def student_manager():
    """Provides a fresh StudentManager for each test."""
    return StudentManager()


class TestAssignments:
    def test_add_assignment_basic(self, student_manager):
        deadline = datetime.now() + timedelta(days=5)

        assignment = student_manager.add_assignment("Math HW", deadline, "Math")

        assert assignment in student_manager.assignments
        assert assignment["title"] == "Math HW"
        assert assignment["subject"] == "Math"
        assert assignment["completed"] is False

    def test_add_assignment_with_empty_title(self, student_manager):
        deadline = datetime.now() + timedelta(days=3)

        assignment = student_manager.add_assignment("", deadline, "Misc")

        # For now we just ensure it is added; behavior can be refined later.
        assert assignment in student_manager.assignments
        assert assignment["title"] == ""

    def test_add_assignment_with_null_title(self, student_manager):
        """Assignment with None as title should still be stored."""
        deadline = datetime.now() + timedelta(days=3)

        assignment = student_manager.add_assignment(None, deadline, "Misc")

        assert assignment in student_manager.assignments
        assert assignment["title"] is None
        assert assignment["completed"] is False

    def test_add_assignment_with_past_deadline(self, student_manager):
        """Assignments in the past should still be tracked."""
        past_deadline = datetime.now() - timedelta(days=1)

        assignment = student_manager.add_assignment(
            "Old HW", past_deadline, "History"
        )

        assert assignment in student_manager.assignments
        assert assignment["deadline"] == past_deadline
        assert assignment["completed"] is False

    def test_list_assignments_empty_collection(self, student_manager):
        # No assignments added yet
        assert student_manager.list_assignments() == []
        assert student_manager.list_assignments(show_completed=True) == []

    def test_list_assignments_shows_only_pending_by_default(self, student_manager):
        deadline = datetime.now() + timedelta(days=5)

        student_manager.add_assignment("A1", deadline)
        student_manager.add_assignment("A2", deadline)
        student_manager.mark_completed("A1")

        pending = student_manager.list_assignments()
        all_assignments = student_manager.list_assignments(show_completed=True)

        assert len(all_assignments) == 2
        assert len(pending) == 1
        assert pending[0]["title"] == "A2"

    def test_mark_completed_existing_assignment(self, student_manager):
        deadline = datetime.now() + timedelta(days=5)

        student_manager.add_assignment("Physics HW", deadline)
        result = student_manager.mark_completed("Physics HW")

        assert result is True
        assert student_manager.assignments[0]["completed"] is True

    def test_mark_completed_non_existent_assignment(self, student_manager):
        deadline = datetime.now() + timedelta(days=5)

        student_manager.add_assignment("Chem HW", deadline)
        result = student_manager.mark_completed("Bio HW")  # not present

        assert result is False  # function should indicate failure

    def test_mark_completed_with_duplicate_titles(self, student_manager):
        deadline = datetime.now() + timedelta(days=5)

        student_manager.add_assignment("Project", deadline)
        student_manager.add_assignment("Project", deadline)

        result = student_manager.mark_completed("Project")

        assert result is True
        # At least one of them should be completed
        completed_count = sum(1 for a in student_manager.assignments if a["completed"])
        assert completed_count >= 1


class TestUpcomingDeadlines:
    def test_upcoming_deadlines_future_assignment(self, student_manager):
        future_deadline = datetime.now() + timedelta(days=3)

        student_manager.add_assignment("Task1", future_deadline)

        upcoming = student_manager.get_upcoming_deadlines(days=7)

        assert len(upcoming) == 1
        assert upcoming[0]["title"] == "Task1"
        # days_remaining and priority are added by get_upcoming_deadlines
        assert "days_remaining" in upcoming[0]
        assert "priority" in upcoming[0]

    def test_upcoming_deadlines_excludes_past_deadline(self, student_manager):
        past_deadline = datetime.now() - timedelta(days=2)

        student_manager.add_assignment("Old Task", past_deadline)

        upcoming = student_manager.get_upcoming_deadlines(days=7)

        # Past tasks should not appear in upcoming deadlines
        assert upcoming == []


class TestGradesAndGPA:
    def test_add_grade_valid(self, student_manager):
        student_manager.add_grade("Math", 90)

        assert len(student_manager.grades) == 1
        assert student_manager.grades[0]["subject"] == "Math"
        assert student_manager.grades[0]["grade"] == 90

    def test_add_grade_negative_value(self, student_manager):
        with pytest.raises(ValueError):
            student_manager.add_grade("Math", -10)

    def test_add_grade_above_max_value(self, student_manager):
        with pytest.raises(ValueError):
            student_manager.add_grade("Math", 150)

    def test_calculate_gpa_with_multiple_grades(self, student_manager):
        student_manager.add_grade("Math", 80)
        student_manager.add_grade("English", 90)
        student_manager.add_grade("Science", 70)

        # Average is (80 + 90 + 70) / 3 = 80
        assert student_manager.calculate_gpa() == pytest.approx(80.0)

    def test_calculate_gpa_with_no_grades(self, student_manager):
        assert student_manager.calculate_gpa() == 0.0


class TestStatistics:
    def test_statistics_with_no_data(self, student_manager):
        stats = student_manager.get_statistics()

        assert stats["total_assignments"] == 0
        assert stats["completed"] == 0
        assert stats["pending"] == 0
        assert stats["gpa"] == 0.0

    def test_statistics_with_assignments_and_grades(self, student_manager):
        deadline = datetime.now() + timedelta(days=5)

        student_manager.add_assignment("Chem", deadline)
        student_manager.add_assignment("Bio", deadline)
        student_manager.mark_completed("Chem")
        student_manager.add_grade("Chem", 90)

        stats = student_manager.get_statistics()

        assert stats["total_assignments"] == 2
        assert stats["completed"] == 1
        assert stats["pending"] == 1
        assert stats["gpa"] == 90
