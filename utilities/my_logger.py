import time
import old.user_input as userInput
import utilities.my_timer as myTimer


# def log_test(logbook_file_path, content):
#     print(content, end = '')#arm MSV
#     with open(logbook_file_path, 'a+') as l1:
#         l1.write(content)
logFileIsCreated = False

def logNewLine(content):
    global logFileIsCreated
    if not logFileIsCreated:
        createNewLogFile()
        logFileIsCreated = True
    with open(userInput.logFilePath, 'a+') as l1:
        l1.write(content + '\n')

def createNewLogFile():
    global logFileIsCreated
    #f = open(myUserInput.logFileName,'w')
    f = open(userInput.logFilePath,'w')
    f.write('Log file created at: ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n\n')
    f.close()
    logFileIsCreated = True

def logNewLineWithTimeStamp(content):
    global logFileIsCreated
    if not logFileIsCreated:
        createNewLogFile()
        logFileIsCreated = True

    with open(userInput.logFilePath, 'a+') as l1:
        message = myTimer.timeSinceT0() + " : " + content + '\n'
        l1.write(message)
        print(message)
