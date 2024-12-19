import mmap #memory mapped file instead of "classic read". Not sure if better in this case but I wanted to use it.
from pathlib import Path

LINKED_CONTENT_START = b'[[' #![[xyz]] is for embedded links, [[]] regular links
LINKED_CONTENT_END = b']]'

referenced = set() #set of filenames referenced in .md files.
vaultPath = None #Path() to Vault directory
attachmentPath = None #Path() to attachment directory

#function used in script to keep it clean.  
def extractAttachmentNames(absoluteFilePath: Path) -> set[str]:
    res = set() #set of attachment names as result
    #check if file is empty by its size. Mmap runs into exception for empty files.
    if absoluteFilePath.stat().st_size == 0:
        return res
    with open(absoluteFilePath) as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapFile:
            posStart = mmapFile.find(LINKED_CONTENT_START) #-1 if not found
            posEnd = mmapFile.find(LINKED_CONTENT_END)
            while posStart >= 0 and posEnd > posStart:
                #here we have found a link and need to check if its linking to another page or a file. (=attachment)
                lenContentName = posEnd - posStart - len(LINKED_CONTENT_START)
                mmapFile.seek(posStart + len(LINKED_CONTENT_START)) #set position in mmapFile
                linkedContentName = mmapFile.read(lenContentName).decode("utf-8") #read length of fileName
                #rudimentary filtering for links containing file extensions. (assumption: extensions are < 6 chars)
                linkedContentNameSplitted = linkedContentName.split(".")
                if len(linkedContentNameSplitted) > 1 and len(linkedContentNameSplitted[-1]) < 6:
                    res.add(linkedContentName)
                posStart = mmapFile.find(LINKED_CONTENT_START, posEnd  +  1)
                posEnd = mmapFile.find(LINKED_CONTENT_END, posEnd + 1)
    return res

################################
# BEGIN SCRIPT
################################

#get vault path
while vaultPath is None or not vaultPath.is_dir():
    vaultPath = Path(input("Vault Directory: "))
print("Vault Path set to: {}".format(vaultPath))

#get attatchment path
while attachmentPath is None or not attachmentPath.is_dir():
    attachmentPath = Path(input("Attachment Directory to check for obsolete files: "))
print("Attachment Path set to: {}".format(attachmentPath))

#walk through vault directory tree. Extract attachment file names from every .md file.  
for (dirPath, dirNames, fileNames) in vaultPath.walk():
    mdFiles = [f for f in fileNames if f.lower().endswith(".md")]
    for fileName in mdFiles:
        absolutePath = Path(dirPath, fileName)
        referenced.update(extractAttachmentNames(absolutePath))

#Scan attachment directory
dirContent = attachmentPath.iterdir() #Generator of Path objects
attachmentFiles = {f.name for f in dirContent if f.is_file()} #set of attachment files in attachment dir.
#Get Difference between referenced and existing att. files -> those are the unreferenced files.
diff = attachmentFiles.difference(referenced)

if len(diff) == 0:
    print("No obsolete files found.")
    quit()

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
    if not obsoleteDirPath.exists():
        obsoleteDirPath.mkdir(parents = True) #creates directory and parent dirs if needed.
    #move files by changing the pathname
    for fname in diff:
        oldPath = Path(attachmentPath, fname)
        newPath = obsoleteDirPath.joinpath(fname)
        print("Moving {0} to: {1}".format(oldPath, newPath))
        Path(attachmentPath, fname).rename(obsoleteDirPath.joinpath(fname)) 
    print("Done")
else:
    #do nothing and end
    print("No action taken.")