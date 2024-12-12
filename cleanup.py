import mmap #memory mapped file prevents the file from being read into memory or having to read line by line
import platform #mmap constructor is os dependend, platform.system() returns OS 'Linux', 'Windows' etc.

referenced = set()
vaultPath = ""
attachmentPath = ""

#get vault path

#get attatchment path

dirQueue = [ vaultPath ]
#while dirQueue not empty
#for every .md file: read every line for [[.something]] string
#how does it look to read a .md file?
os = platform.system()
with open("/home/sebastian/Projects/Python/VaultCleanup/sample.md") as file:
    if os == "Linux":
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as asByteArray:
            print(asByteArray)
            posStart = asByteArray.find(b'![[Pasted image')
            posEnd = asByteArray.find(b']]', posStart)
            print("Start: {} End: {}".format(posStart, posEnd))





#for every directory: add to queue



#move every non referenced file to attachmentPath/obsolete dir

# What we search for:
# - **read-only** Attribute können in [[UML]] via `{readOnly}` Angabe beschrieben werden.
# ![[Pasted image 20241121161004.png]]
#
#