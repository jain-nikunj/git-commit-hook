"""
MIT License

Copyright (c) 2017 Nikunj Jain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
#!/usr/bin/python
import re
import sys
import subprocess

branchName = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
branchName = branchName[2:len(branchName) - 2]

commitFile = sys.argv[1]
sys.stdin = open("/dev/tty", "r")

allowedType = ['feat', 'maint', 'fix', 'impr']
dictHelpMsg = {'feat': "A new feature",
               'fix': "A bug fix",
               'maint': ( 'Any maintenance like: \n' +
                                '(docs) Documentation changes\n' +
                                "(tests) Adding missing or correcting existing tests\n" + 
                                "(chore) Changes to the build process or auxiliary tools and libraries such as documentation generation\n"),
               'impr': ( 'Improvements like: \n' +
                                '(style) Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)\n' +
                                '(performance) Changes that affect the performance of the code\n' +
                                '(refactoring) Refactoring of code'
                              )
              }

if not branchName == 'master':
  allowedType.append("quick")
  dictHelpMsg['quick'] = "A quick commit made for temporary changes"

nameErrorMsg = "Github usernames may not contain spaces and need '@'.\n"
typeErrorMsg = ("Incorrect format for commit type.\n" +
  "You can avoid such messages in the future by following this format in your messages: 'COMMIT_TYPE: COMMIT_SUBJECT'\n" +
  "Choose from the following:\n" +
  str(allowedType) + "\nPlease enter a new commit type, or enter 'help' for details on what each type means: ")
subjectErrorMsg = "Incorrect format for commit subject.\nPlease enter message subject:"
isPPMsg = "Were you pair programming? [y/n]: "
driverMsg = "Enter the Github email ID of the driver: "
observerMsg = "Enter the Github email ID of the observer: "

with open(commitFile) as f:
  flag = False
  commitSubjectMsg = f.readline()
  commitBodyMsg = ""
  for line in f.readlines():
    if not re.match("#.*", line):
      commitBodyMsg += line

  commitMsgSplit = commitSubjectMsg.split(':')
  try:
    msgType, msgSubject = commitMsgSplit[:2]
  except ValueError as e:
    flag = True
    msgType = raw_input(typeErrorMsg)

  typeMatch = any([re.match(".*" + word.lower() + ".*", msgType.lower().lstrip()) for word in allowedType])

  while not typeMatch:
    if re.match(".*help.*", msgType.lower().lstrip()):
      print('\n')
      [print(key + ": " + dictHelpMsg[key] + "\n") for key in allowedType]

    msgType = raw_input(typeErrorMsg)
    typeMatch = any([re.match(".*" + word.lower() + ".*", msgType.lower().lstrip()) for word in allowedType])

  if flag:
    msgSubject = raw_input(subjectErrorMsg).lstrip()
    commitMsgSplit = [msgType, msgSubject]

  commitMsgSplit.append(raw_input(isPPMsg))

  noPPMsg = re.match("[^yn].*", commitMsgSplit[2].lower().lstrip())

  while noPPMsg:
    commitMsgSplit[2] = raw_input(isPPMsg).lstrip().lower()
    noPPMsg = re.match("[^yn].*", commitMsgSplit[2])

  isPP = re.match("y.*", commitMsgSplit[2].lower().lstrip())

  if isPP:
    driver = raw_input(driverMsg)
    while re.match(".* .*", driver) or not re.match("[^@]+@[^@]+\.[^@]+", driver):
      print(nameErrorMsg)
      driver = raw_input(driverMsg)

    observer = raw_input(observerMsg)
    while re.match(".* .*", observer) or not re.match("[^@]+@[^@]+\.[^@]+", observer):
      print(nameErrorMsg)
      observer = raw_input(observerMsg)

with open(commitFile, "w+") as f:
  f.write(msgType + ": ")
  f.write(msgSubject + "\n")
  f.write(commitBodyMsg)

  if isPP:
    f.write("DRIVER: " + driver + "\n")
    f.write("OBSERVER: " + observer + "\n")

