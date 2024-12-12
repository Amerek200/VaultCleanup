import mmap #memory mapped file prevents the file from being read into memory or having to read line by line
import platform #mmap constructor is os dependend, platform.system() returns OS 'Linux', 'Windows' etc.
import os

PASTED_IMAGE_START = b'![[Pasted image'
PASTED_IMAGE_END = b']]'

referenced = set()
vaultPath = "/home/sebastian/Projects"
attachmentPath = "/home/sebastian/Projects"
osName = platform.system() #"Windows" or "Linux" for my use case

                    
def extractAttachmentNames(absoluteFilePath: str) -> set[str]:
    res = set()
    with open(absoluteFilePath) as file:
        if osName == "Linux": #2D: set param according to OS
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapFile:
                posStart = mmapFile.find(PASTED_IMAGE_START) #-1 if not found
                posEnd = mmapFile.find(PASTED_IMAGE_END)
                while posStart >= 0 and posEnd > posStart:
                    #better to use split() instead of this magic numbers?
                    #16 = offset to remove "![[Pasted image "
                    lenAttFileName = posEnd - posStart - 16
                    mmapFile.seek(posStart + 16) #set position in mmapFile
                    attFileName = mmapFile.read(lenAttFileName) #read length of fileName
                    res.add(attFileName.decode("utf-8"))
                    posStart = mmapFile.find(PASTED_IMAGE_START, posEnd  +  1)
                    posEnd = mmapFile.find(PASTED_IMAGE_END, posEnd + 1)
    return res

################################
# BEGIN SCRIPT
################################

#get vault path
while not os.path.isdir(vaultPath):
    vaultPath = input("Vault Directory: ")
print("Vault Path set to: {}".format(vaultPath))

#get attatchment path
while not os.path.isdir(attachmentPath):
    attachmentPath = input("Attachment Directory to check for obsolete files: ")
print("Attachment Path set to: {}".format(attachmentPath))

#os.listdir to list every element in dir
#queue not needed if we can use os.walk
#os.path.join(dirpath, name) to get absolute path

for (dirPath, dirNames, fileNames) in os.walk(vaultPath):
    mdFiles = [f for f in fileNames if f.lower().endswith(".md")]
    for fileName in mdFiles:
        absolutePath = os.path.join(dirPath, fileName)
        referenced.update(extractAttachmentNames(absolutePath))
    
print("done")


        
#40: ![[Pasted image 20241115154748.png]]\n- K

#scan every .md file for string

#while dirQueue not empty
#for every .md file: read every line for [[.something]] string
#how does it look to read a .md file?
#with open("/home/sebastian/Projects/Python/VaultCleanup/sample.md") as file:





#for every directory: add to queue



#move every non referenced file to attachmentPath/obsolete dir

# What we search for:
# - **read-only** Attribute können in [[UML]] via `{readOnly}` Angabe beschrieben werden.
# ![[Pasted image 20241121161004.png]]
#
#