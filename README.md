# git-commit-hook
A commit-hook which will error check a standard Git commit message.

# Usage
Copy the executable file `commit-msg` into `/path/to/your/repo/.git/hooks/`

# For Developers
The file `commit-msg.py` contains the scripting necessary for basic regex checking.
To generate the executable, execute:
  `pyinstaller commit-msg.py --onefile`
