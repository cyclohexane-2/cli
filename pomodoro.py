"""
Pomodoro timer for StudentHub with ASCII splash and interactive menu.
"""
import time
import sys
import subprocess
import shutil
import threading
import platform
import os
from datetime import timedelta

PLATFORM = platform.system().lower()

ASCII_SPLASH = r"""
    __________                         .___                   
    \______   \____   _____   ____   __| _/___________  ____  
    |     ___/  _ \ /     \ /  _ \ / __ |/  _ \_  __ \/  _ \ 
    |    |  (  <_> )  Y Y  (  <_> ) /_/ (  <_> )  | \(  <_> )
    |____|   \____/|__|_|  /\____/\____ |\____/|__|   \____/ 
                         \/            \/                               
     even einstein used to follow the pomodoro technique
                    just saying
  
"""

class PomodoroTimer:
    """
    Pomodoro timer with optional interactive menu and ASCII art splash.
    """
    def __init__(self, work_minutes=25, break_minutes=5, sound=True, notifier_cmd=None):
        """Initialize timer settings and notifier."""
        self.work_minutes = int(work_minutes)
        self.break_minutes = int(break_minutes)
        self.sound = bool(sound)
        self._stop_requested = False
        self.notifier_cmd = notifier_cmd or self._detect_notifier()
    def _detect_notifier(self):
        if PLATFORM == "linux" and shutil.which("notify-send"): return "notify-send"
        if PLATFORM == "darwin" and shutil.which("osascript"): return "osascript"
        if PLATFORM == "windows" and shutil.which("powershell"): return "powershell"
        return None
    def _notify(self, title, message):
        try:
            if PLATFORM == "linux" and self.notifier_cmd == "notify-send":
                subprocess.Popen(["notify-send", title, message])
            elif PLATFORM == "darwin" and self.notifier_cmd == "osascript":
                subprocess.Popen(["osascript","-e",f'display notification "{message}" with title "{title}"'])
            elif PLATFORM == "windows" and self.notifier_cmd == "powershell":
                ps='Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show("{}","{}")'.format(message,title)
                subprocess.Popen(["powershell","-NoProfile","-Command",ps],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except:
            pass
        print(f"\n=== {title} ===\n{message}\a\n",flush=True)
    def _play_sound(self):
        if not self.sound: return
        try:
            if PLATFORM == "linux":
                for p in ("paplay","aplay","play"):
                    if shutil.which(p):
                        path="/usr/share/sounds/freedesktop/stereo/complete.oga"
                        if os.path.exists(path):
                            subprocess.Popen([p,path],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                            return
                sys.stdout.write("\a"); sys.stdout.flush()
            elif PLATFORM == "darwin":
                if shutil.which("afplay"):
                    for p in ("/System/Library/Sounds/Glass.aiff","/System/Library/Sounds/Pop.aiff"):
                        if os.path.exists(p):
                            subprocess.Popen(["afplay",p],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                            return
                sys.stdout.write("\a"); sys.stdout.flush()
            elif PLATFORM == "windows":
                try:
                    import winsound
                    winsound.MessageBeep(winsound.MB_ICONASTERISK)
                except:
                    try:
                        winsound.Beep(1000,300)
                    except:
                        sys.stdout.write("\a"); sys.stdout.flush()
            else:
                sys.stdout.write("\a"); sys.stdout.flush()
        except:
            sys.stdout.write("\a"); sys.stdout.flush()
    def _format_mmss(self, s):
        if s < 0: s = 0
        m, s = divmod(int(s), 60)
        return f"{m:02d}:{s:02d}"
    def _countdown(self, total_seconds, label="Working"):
        end = time.time() + float(total_seconds)
        try:
            while time.time() < end:
                if self._stop_requested: return False
                remaining = end - time.time()
                mmss = self._format_mmss(remaining)
                sys.stdout.write(f"\r{label} — {mmss} remaining   ")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\r" + " " * 60 + "\r")
            sys.stdout.flush()
            return True
        except KeyboardInterrupt:
            self._stop_requested = True
            print("\nTimer cancelled by user.")
            return False
    def _show_splash(self):
        print(ASCII_SPLASH)
    def _interactive_menu(self):
        sessions = self.work_minutes and 4 or 4
        work = self.work_minutes
        brk = self.break_minutes
        sound = self.sound
        while True:
            os.system('cls' if platform.system().lower()=="windows" else 'clear')
            self._show_splash()
            print(f"Current: sessions = {sessions}, work = {work} minutes, break = {brk} minutes, sound = {'on' if sound else 'off'}")
            print("Options:")
            print("  1) Start now")
            print("  2) Configure sessions/work/break")
            print("  3) Toggle sound on/off")
            print("  4) Quick test (6s work / 4s break)")
            print("  5) Quit")
            try:
                choice = input("Choose [1-5]: ").strip()
            except KeyboardInterrupt:
                print("\nInterrupted by user, shoulda thought before starting heh...")
                return None
            if choice == "1":
                return {"sessions": sessions, "work": work, "break": brk, "sound": sound}
            if choice == "2":
                try:
                    ns = input(f"Sessions ({sessions}): ").strip()
                    if ns: sessions = int(ns)
                    nw = input(f"Work minutes ({work}): ").strip()
                    if nw: work = float(nw)
                    nb = input(f"Break minutes ({brk}): ").strip()
                    if nb: brk = float(nb)
                except ValueError:
                    input("Invalid number, press Enter to continue...")
                    continue
            if choice == "3":
                sound = not sound
            if choice == "4":
                return {"sessions":1,"work":0.1,"break":0.0667,"sound":sound}
            if choice == "5":
                return None
    def start(self, sessions=4, work_minutes=None, break_minutes=None, interactive=False):
        if interactive:
            opts = self._interactive_menu()
            if not opts:
                print("Cancelled.")
                return
            sessions = int(opts["sessions"])
            work_minutes = opts["work"]
            break_minutes = opts["break"]
            self.sound = bool(opts["sound"])
        if work_minutes is not None: self.work_minutes = int(work_minutes) if float(work_minutes).is_integer() else work_minutes
        if break_minutes is not None: self.break_minutes = int(break_minutes) if float(break_minutes).is_integer() else break_minutes
        sessions = int(sessions)
        print(f"Starting Pomodoro: {sessions} sessions — {self.work_minutes}m work / {self.break_minutes}m break")
        try:
            for s in range(1, sessions + 1):
                if self._stop_requested: break
                print(f"\nSession {s} — Work ({self.work_minutes} minutes)")
                if not self._countdown(self.work_minutes * 60, f"Work (Session {s}/{sessions})"): break
                self._play_sound(); self._notify("Work done","Time for a break!")
                if s == sessions:
                    print("All sessions complete. Good job!"); self._notify("Pomodoro","All sessions complete!"); break
                print(f"Break — {self.break_minutes} minutes")
                if not self._countdown(self.break_minutes * 60, f"Break (Session {s}/{sessions})"): break
                self._play_sound(); self._notify("Break finished","Next session starting")
        except KeyboardInterrupt:
            print("\nPomodoro interrupted by user.")
        finally:
            print("Pomodoro stopped.")
    def start_in_thread(self, *args, **kwargs):
        t = threading.Thread(target=self.start, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--sessions","-s",type=int,default=1)
    p.add_argument("--work",type=float,default=0.1)
    p.add_argument("--break",dest="brk",type=float,default=0.1)
    p.add_argument("--no-sound",action="store_true")
    args = p.parse_args()
    timer = PomodoroTimer(work_minutes=args.work, break_minutes=args.brk, sound=not args.no_sound)
    timer.start(sessions=args.sessions, work_minutes=args.work, break_minutes=args.brk, interactive=True)
