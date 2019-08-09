import sys
from jsbeautifier import beautify_file
from subprocess import Popen, PIPE

def lintFiles():
    argLen = len(sys.argv)
    if(argLen < 2):
        print('Please include a filename')
        return
    for i in range(1,argLen):
        filename = sys.argv[i]
        print('linting ' + str(filename))
        runLinter(filename)

def runLinter(filename):
    res = beautify_file(filename)
    with open(filename,'w') as file:
        file.write(res)
    cmd = ["/eerun/bin/checkjs",filename] 
    process = Popen(cmd, stdout=PIPE,stderr=PIPE)
    stdout,stderr =  process.communicate()
    outputList = stdout.splitlines()
    parseOutput(outputList,filename)

def parseOutput(lst,filename):
    locations = []
    for line in lst:
        words = line.split(' ')
        lastWord = words[len(words) - 1]
        needsSemicolon = lastWord == 'semicolon.'
        if(needsSemicolon):
            lineNumber = int(words[2].replace(',',''))
            colNumber = int(words[4].replace(',',''))
            locations.append((lineNumber,colNumber))
    addSemicolons(locations,filename)

def addSemicolons(locations,filename):
    with open(filename,'rU') as file:
        data = file.readlines()
        for loc in locations:
            lineNumber = loc[0]
            colNumber = loc[1]
            data[lineNumber-1] = data[lineNumber-1].rstrip() + ';\n'
        out = open(filename,'w')
        out.writelines(data)
        out.close()

lintFiles()
