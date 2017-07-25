# git-commit-hook
A commit-hook which will error check a standard Git commit message.  
Built by Nikunj Jain under the guidance of Hezheng Yin.

# For Users
Depending on your python version, copy the executable file `pythonX/commit-msg` into `/path/to/your/repo/.git/hooks/`  
The format for commit messages is as follows:  
```
COMMIT_TYPE: COMMIT_SUBJECT  
COMMIT BODY  
```
Commit type may include: `'feat', 'fix', 'maint', 'impr'`  
Note: An extra commit type, `'quick'`, is available if you are not working on master.  
The executable will always prompt you regarding whether you were Pair Programming or
not, and will prompt for and append the Driver and Observer to the end of the
commit body if you answer yes.  
<dl>
  <dt><strong>(feat) New Feature</strong></dt>
    <dd>A new feature </dd>
  <dt><strong>(fix) Bug Fix</strong></dt>
    <dd>Bug fixes</dd>
  <dt><strong>(maint) Maintenance</strong></dt>
    <dd>Any maintenance like: <br> 
        (docs) Documentation changes <br>
        (tests) Adding missing or correcting existing tests <br>
        (chore) Changes to the build process or auxiliary tools and libraries </dd>
  <dt><strong>(impr) Improvements like: </strong></dt>
    <dd>(style) Changes that do not affect the meaning of the code (white-space, formatting, semi-colons, etc <br>
        (performance) Changes that affect the performance of the code <br>
        (refactoring) Refactoring changes in the code </dd>
  <dt><strong>(quick) Quick Commit </strong></dt>
    <dd> A quick and dirty commit, to be updated later (for things like daily stash of changes) </dd>
</dl>

# For Developers Looking to Add to the Project
The file `commit-msg.py` contains the scripting necessary for basic regex checking.
To generate the executable, execute: `pyinstaller commit-msg.py --onefile`
