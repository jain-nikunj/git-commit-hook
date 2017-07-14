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
#!/usr/bin/python3
import re
import sys
import subprocess

branchName = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
branchName = branchName[2:len(branchName) - 2]

commitFile = sys.argv[1]
sys.stdin = open("/dev/tty", "r")

allowedType = ['feat', 'fix', 'docs', 'style', 'test', 'chore']
dictHelpMsg = {'feat': "A new feature",
               'fix': "A bug fix",
               'docs': 'Documentation only changes',
               'style': 'Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)',
               'test': "Adding missing or correcting existing tests",
               'chore': "Changes to the build process or auxiliary tools and libraries such as documentation generation"
              }

if not branchName == 'master':
  allowedType.append("quick")
  dictHelpMsg['quick'] = "A quick commit made for temporary changes"

nameErrorMsg = "Github usernames may not contain spaces.\n"
typeErrorMsg = ("Incorrect format for commit type.\n" +
  "You can avoid such messages in the future by following this format in your messages: 'COMMIT_TYPE: COMMIT_BODY; PAIR_PROGRAMMING [yes/no]'\n" + 
  "Choose from the following:\n" +
  str(allowedType) + "\nPlease enter a new commit type, or enter 'help' for details on what each type means: ")
bodyErrorMsg = "Incorrect format for commit body.\nPlease enter message body:\n"
isPPMsg = "Were you pair programming? "
driverMsg = "Enter the Github username of the driver: "
observerMsg = "Enter the Github username of the observer: "

with open(commitFile) as f:
  flag = False
  commitMsg = ""
  for line in f.readlines():
    if not re.match("#.*", line):
      commitMsg += line

  commitMsgSplit = commitMsg.split(':')
  try:
    msgType, msgBody = commitMsgSplit[:2]
  except ValueError as e:
    flag = True
    msgType = input(typeErrorMsg)

  typeMatch = any([re.match(".*" + word.lower() + ".*", msgType.lower().lstrip()) for word in allowedType])

  while not typeMatch:
    if re.match(".*help.*", msgType.lower().lstrip()):
      [print(key + ": " + value + "\n") for key, value in dictHelpMsg.items()]

    msgType = input(typeErrorMsg)
    typeMatch = any([re.match(".*" + word.lower() + ".*", msgType.lower().lstrip()) for word in allowedType])

  if flag:
    msgBody = input(bodyErrorMsg).lstrip()
    commitMsgSplit = [msgType, msgBody]
  else:
    commitMsgSplit = [msgType] + commitMsgSplit[1].split(";")
    msgBody = commitMsgSplit[1].lstrip()

  if len(commitMsgSplit) < 3:
    commitMsgSplit.append(input(isPPMsg))

  noPPMsg = re.match("[^yn].*", commitMsgSplit[2].lower().lstrip())

  while noPPMsg:
    commitMsgSplit[2] = input(isPPMsg).lstrip().lower()
    noPPMsg = re.match("[^yn].*", commitMsgSplit[2])

  isPP = re.match("y.*", commitMsgSplit[2].lower().lstrip())

  if isPP:
    driver = input(driverMsg)
    while re.match(".* .*", driver):
      print(nameErrorMsg)
      driver = input(driverMsg)

    observer = input(observerMsg)
    while re.match(".* .*", observer):
      print(nameErrorMsg)
      observer = input(observerMsg)

with open(commitFile, "w+") as f:
  f.write(msgType + ":")
  f.write(msgBody + ";")
  f.write(str(bool(isPP)) + ";")

  if isPP:
    f.write(driver + ";")
    f.write(observer + ";")

