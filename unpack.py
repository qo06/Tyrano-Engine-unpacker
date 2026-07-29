from struct import unpack
from json import loads
from os import makedirs
from os.path import sep,abspath
import sys

def FolderLoop(Data='',Current='',sf=0) -> list:
    OutList = []
    Data = Data['files']
    for i in Data.items():

        # Check if this is a folder or not.
        if list(i[1].items())[0][0] == 'files':
            OutList.append([ Current + sep + i[0] , 0 , 0])
            OutList += FolderLoop( i[1],\
                                  Current = Current + sep + i[0] ,\
                                   sf=sf)
        else:
            Size   = list(i[1].items())[0][1]
            Offset = list(i[1].items())[1][1]

            OutList.append([ Current + sep + i[0],\
                             Size,\
                             int(Offset) + sf ])
    return OutList

def extract(File,OutDir=""):

    ExecPath = File.split(".")[0] + sep
    
    fr = open(File,'rb')
    
    #with open(File,'rb') as fr:

    _,val_2,_,IndexSize = unpack('<IIII',fr.read(16))
        
    fr.seek(16,0)
        
    Index =  loads( fr.read(IndexSize).decode('utf8') )
    Index = FolderLoop(Index,Current='',sf=val_2+8)
        
    for i in Index:
        print(i[0])
        EntryName,Size,Offset = i
        Path = ExecPath + EntryName
        if (Size,Offset) == (0,0):
            makedirs(EntryName,exist_ok=True)
        else:
            fr.seek(Offset,0)
            Data = fr.read(Size)
            
            fw = open(Path,'wb')
            fw.write(Data)
            fw.close()
    fr.close()

if __name__ == '__main__':
    extract(sys.argv[1])