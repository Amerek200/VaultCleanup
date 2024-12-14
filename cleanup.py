#maybe todos: Benachmark reg. I/O vs. mmap, allow setting of (attachment) file extension 
#check wants to move EVERYTHING to obs. something in my check must bew wrong

import mmap #memory mapped file instead of "classic read". Not sure if better in this case but I wanted to use it.
import os
from pathlib import Path

PASTED_IMAGE_START = b'![[Pasted image '
PASTED_IMAGE_END = b']]'

referenced = set()
vaultPath = Path("C:/Users/sebad/OneDrive/Dokumente/Obsidian Vault") #"/home/sebastian/Projects" #restore to ""
attachmentPath = Path('C:/Users/sebad/OneDrive/Dokumente/Obsidian Vault/Anhaenge') #"/home/sebastian/Projects" #restore to ""

                    
def extractAttachmentNames(absoluteFilePath: Path) -> set[str]:
    res = set()
    #check if file is empty by its size. Mmap runs into exception for empty files.
    if absoluteFilePath.stat().st_size == 0:
        return res
    with open(absoluteFilePath) as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapFile:
            posStart = mmapFile.find(PASTED_IMAGE_START) #-1 if not found
            posEnd = mmapFile.find(PASTED_IMAGE_END)
            while posStart >= 0 and posEnd > posStart:
                #better to use split() instead of this magic numbers?
                #16 = offset to remove "![[Pasted image "
                lenAttFileName = posEnd - posStart - len(PASTED_IMAGE_START)
                mmapFile.seek(posStart + len(PASTED_IMAGE_START)) #set position in mmapFile
                attFileName = mmapFile.read(lenAttFileName) #read length of fileName
                res.add(attFileName.decode("utf-8"))
                posStart = mmapFile.find(PASTED_IMAGE_START, posEnd  +  1)
                posEnd = mmapFile.find(PASTED_IMAGE_END, posEnd + 1)
    return res

################################
# BEGIN SCRIPT
################################

#get vault path
while not vaultPath.is_dir():
    vaultPath = Path(input("Vault Directory: "))
print("Vault Path set to: {}".format(vaultPath))

#get attatchment path
while not attachmentPath.is_dir():
    attachmentPath = Path(input("Attachment Directory to check for obsolete files: "))
print("Attachment Path set to: {}".format(attachmentPath))

#os.listdir to list every element in dir
#queue not needed if we can use os.walk
#os.path.join(dirpath, name) to get absolute path

for (dirPath, dirNames, fileNames) in vaultPath.walk():
    mdFiles = [f for f in fileNames if f.lower().endswith(".md")]
    for fileName in mdFiles:
        absolutePath = Path(dirPath, fileName)
        referenced.update(extractAttachmentNames(absolutePath))

#Scan attachment directory
dirContent = attachmentPath.iterdir()
attachmentFiles = {f for f in dirContent if Path(attachmentPath, f).is_file()}
#Get Difference between referenced and existing att. files
diff = attachmentFiles.difference(referenced)

#print obsolete files
print("potential obsolete files:")
for fName in diff:
    print(fName)

print("#######################")
obsoleteDirName = input("Directory name for obsolete files: ")
obsoleteDirPath = Path(attachmentPath, obsoleteDirName)
#invalid if path exsists and is not a directoy
while obsoleteDirPath.exists() and not obsoleteDirPath.is_dir():
    obsoleteDirName = input("Invalid directroy name {0}. \nDirectroy name for obsolete files: ".format(obsoleteDirPath))
    obsoleteDirPath = Path(attachmentPath, obsoleteDirName)

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