#maybe todos: Benachmark reg. I/O vs. mmap, allow setting of (attachment) file extension 


import mmap #memory mapped file instead of "classic read". Not sure if better in this case but I wanted to use it.
import platform #mmap constructor is os dependend, platform.system() returns OS 'Linux', 'Windows' etc.
import os

PASTED_IMAGE_START = b'![[Pasted image'
PASTED_IMAGE_END = b']]'

referenced = set()
vaultPath = "C:/Users/sebad/OneDrive/Dokumente/Obsidian Vault" #"/home/sebastian/Projects" #restore to ""
attachmentPath = 'C:/Users/sebad/OneDrive/Dokumente/Obsidian Vault/Anhaenge' #"/home/sebastian/Projects" #restore to ""
osName = platform.system() #"Windows" or "Linux" for my use case

                    
def extractAttachmentNames(absoluteFilePath: str) -> set[str]:
    res = set()
    with open(absoluteFilePath) as file:
        if osName == "Linux" or osName == "Windows": #2Do: set param according to OS
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

#Scan attachment directory
dirContent = os.listdir(attachmentPath)
attachmentFiles = {f for f in dirContent if os.path.isfile( os.path.join(attachmentPath, f) )}
#Get Difference between referenced and existing att. files
diff = attachmentFiles.difference(referenced)

#print obsolete files
print("potential obsolete files:")
for fName in diff:
    print(fName)

print("#######################")
obsoleteDirName = input("Directory name for obsolete files: ")
obsoleteDirPath = os.path.join(attachmentPath, obsoleteDirName)
#invalid if path exsists and is not a directoy
while os.path.exists(obsoleteDirPath) and not os.path.isdir(obsoleteDirPath):
    obsoleteDirName = input("Invalid directroy name {0}. \nDirectroy name for obsolete files: ".format(obsoleteDirPath))
    obsoleteDirPath = os.path.join(attachmentPath, obsoleteDirName)

confirmation = input("moving {0} files to {1}. Type \"y\" to confirm, everything else to stop: ".format(len(diff), obsoleteDirPath))
if confirmation == "y":
    #move files
    print("YEP")
else:
    #do nothing and end
    print("No action taken.")
print("done")


        
#40: ![[Pasted image 20241115154748.png]]\n- K
# What we search for:
# - **read-only** Attribute können in [[UML]] via `{readOnly}` Angabe beschrieben werden.
# ![[Pasted image 20241121161004.png]]
#
#