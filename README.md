# git-commit-hook
A commit-hook which will error check a standard Git commit message.  
Built by Nikunj Jain under the guidance of Hezheng Yin.

# Usage
Copy the executable file `commit-msg` into `/path/to/your/repo/.git/hooks/`  
The format for commit messages is as follows:  
```
COMMIT_TYPE: COMMIT_SUBJECT  
COMMIT BODY  
```
Commit type may include: `'feat', 'fix', 'docs', 'style', 'test', 'chore'`  
Note: An extra commit type, `'quick'`, is available if you are not working on master.  
The executable will always prompt you regarding whether you were Pair Programming or
not, and will prompt for and append the Driver and Observer to the end of the
commit body if you answer yes.  

# For Developers
The file `commit-msg.py` contains the scripting necessary for basic regex checking.
To generate the executable, execute: `pyinstaller commit-msg.py --onefile`
