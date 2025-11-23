# Quick Start Guide - StudentHub

## For Students Attending the Workshop

This is a **5-minute quick start** to get you contributing!

---

## Step 1: Setup (2 minutes)

### Check Python Installation
```bash
python --version
```
You need Python 3.7 or higher. If not installed, download from [python.org](https://www.python.org/downloads/)

### Clone/Download the Project
```bash
cd your-workspace-folder
# If you have the project already, just navigate to it
cd demo
```

---

## Step 2: Run the Code (1 minute)

### See Available Commands
```bash
python main.py --help
```

### Try Some Commands
```bash
# Add an assignment
python main.py add-assignment "Physics Lab" --deadline "2025-12-15" --subject "Physics"

# List assignments (Note: won't work yet - this is a bug to fix!)
python main.py list

# Check statistics
python main.py stats

# Calculate GPA
python main.py gpa
```

---

## Step 3: Run Tests (30 seconds)

```bash
# Run the unit tests
python -m pytest tests/ -v

# OR using unittest
python -m unittest tests/test_utils.py
```

Expected output: **4 tests passed** ✓

---

## Step 4: Pick Your First Issue (1 minute)

Open `ISSUES.md` and choose based on your comfort level:

### Never coded before? Start here:
- **Issue #2**: Fix documentation typo (just edit text!)
- **Issue #4**: Add a docstring (copy-paste example)

### Some Python knowledge?
- **Issue #1**: Add error handling (try-except block)
- **Issue #3**: Add input validation

### Comfortable with Python?
- **Issue #5**: Implement delete feature
- **Issue #6**: Write unit tests

---

## Step 5: Make Your First Contribution (During Workshop)

### Create a Branch
```bash
git checkout -b fix-issue-2
```

### Make Your Changes
Edit the file mentioned in the issue

### Test Your Changes
```bash
python main.py --help
python -m pytest tests/
```

### Commit and Push
```bash
git add .
git commit -m "Fix: Update README placeholder (Issue #2)"
git push origin fix-issue-2
```

---

## Common Commands Reference

| Task | Command |
|------|---------|
| See all commands | `python main.py --help` |
| Add assignment | `python main.py add-assignment "Title" --deadline "2025-12-01"` |
| List assignments | `python main.py list` |
| Mark complete | `python main.py complete "Title"` |
| Check GPA | `python main.py gpa` |
| See statistics | `python main.py stats` |
| Run tests | `python -m pytest tests/ -v` |

---

## Known Issues (By Design!)

These are **intentional bugs** for you to fix:

1. ❌ Data doesn't persist (Issue #8)
2. ❌ Invalid dates crash the program (Issue #1)
3. ❌ No way to delete assignments (Issue #5)
4. ❌ Missing documentation (Issues #2, #4)
5. ❌ No colored output (Issue #7)

---

## Quick Testing Tips

### Test Error Handling (for Issue #1)
```bash
# This WILL crash (that's the bug!)
python main.py add-assignment "Test" --deadline "invalid-date"
```

After you fix Issue #1, it should show an error message instead of crashing.

### Test Validation (for Issue #3)
```python
# Open Python interpreter
python

# Run this code
from student_manager import StudentManager
manager = StudentManager()

# This should work
manager.add_grade("Math", 95)

# These should fail gracefully (after you fix Issue #3)
manager.add_grade("Math", -5)    # Negative grade
manager.add_grade("Math", 150)   # Too high
manager.add_grade("Math", "A+")  # Wrong type
```

---

## Need Help?

1. Read `CONTRIBUTING.md` for detailed steps
2. Check `ISSUES.md` for issue descriptions
3. Ask your instructor/mentor
4. Comment on the issue you're working on

---

## Pro Tips

✅ **Start small** - Issue #2 takes 30 seconds!
✅ **Read the code first** - Understand before changing
✅ **Test your changes** - Run the program and tests
✅ **One issue at a time** - Don't mix multiple fixes
✅ **Ask questions** - No question is too small!

---

## What Makes This Project Good for Learning?

1. **Real code** - Actual Python project, not a toy example
2. **Clear issues** - Each issue teaches specific skills
3. **Immediate feedback** - Run code and see results instantly
4. **Progressive difficulty** - Start easy, level up
5. **Practical skills** - CLI tools, testing, documentation

---

## Time Estimates

| Task | Time |
|------|------|
| Setup environment | 2-5 min |
| Fix Issue #2 (typo) | 1 min |
| Fix Issue #4 (docstring) | 3 min |
| Fix Issue #1 (error handling) | 10 min |
| Fix Issue #3 (validation) | 15 min |
| Fix Issue #5 (delete feature) | 30 min |
| Fix Issue #6 (unit tests) | 45 min |

---

## After the Workshop

Once you're comfortable:
1. Complete 2-3 more issues
2. Try the advanced issues (#8-#10)
3. Create your own feature!
4. Find a real open source project on GitHub
5. Apply the same skills you learned here

**Remember**: Every expert was once a beginner who didn't give up!

Happy coding! 🚀
