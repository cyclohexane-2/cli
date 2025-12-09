"""
StudentHub - CLI Entry Point
"""

import argparse
from student_manager import StudentManager
from utils import format_date, save_to_json, load_from_json
from pomodoro import PomodoroTimer


def main():
    parser = argparse.ArgumentParser(description='StudentHub - Manage your academic life')

    parser.add_argument('command', choices=['add-assignment', 'list', 'complete', 'gpa', 'stats','pomodoro'],
                        help='Command to execute')
    parser.add_argument('value', nargs='?', help='Value for the command')
    parser.add_argument('--deadline', help='Deadline in YYYY-MM-DD format')
    parser.add_argument('--subject', help='Subject name')
    parser.add_argument('--sessions', type=int, default=4)
    parser.add_argument('--work',type=int,default=25)
    parser.add_argument('--break-minutes',type=int,default=5)
    parser.add_argument('--no-sound',action='store_true')
    

    args = parser.parse_args()

    manager = StudentManager()

    if args.command == 'add-assignment':
        if not args.value or not args.deadline:
            print("Error: Please provide assignment title and deadline")
            return

        deadline = format_date(args.deadline)
        assignment = manager.add_assignment(args.value, deadline, args.subject)
        print(f"Added assignment: {assignment['title']}")

    elif args.command == 'list':
        assignments = manager.list_assignments()
        if not assignments:
            print("No pending assignments!")
        else:
            for assignment in assignments:
                print(f"- {assignment['title']} (Due: {assignment['deadline']})")

    elif args.command == 'complete':
        if manager.mark_completed(args.value):
            print(f"Marked '{args.value}' as completed!")
        else:
            print(f"Assignment '{args.value}' not found")

    elif args.command == 'gpa':
        gpa = manager.calculate_gpa()
        print(f"Your current GPA: {gpa:.2f}")

    elif args.command == 'stats':
        stats = manager.get_statistics()
        print("=== Your Statistics ===")
        print(f"Total Assignments: {stats['total_assignments']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")
        print(f"GPA: {stats['gpa']:.2f}")
    elif args.command == 'pomodoro':
        timer = PomodoroTimer(
            work_minutes=args.work,
            break_minutes=args.break_minutes,
            sound=not args.no_sound
        )
        timer.start(interactive=True)

if __name__ == '__main__':
    main()
