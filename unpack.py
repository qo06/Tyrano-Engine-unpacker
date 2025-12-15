from struct import unpack
from json import loads
from os import makedirs,getcwd
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
    
    with open(File,'rb') as fr:

        _,val_2,_,IndexSize = unpack('<IIII',fr.read(16))
        
        fr.seek(16,0)
        
        Index =  loads( fr.read(IndexSize).decode('utf8') )

        Index = FolderLoop(Index,\
                           Current='',\
                           sf=val_2+8)
        
        for i in Index:
            print(i[0])
            Path = ExecPath + i[0]
            if i[1] == 0 and i[2] == 0:
                makedirs(Path,exist_ok=True)
            else:
                fr.seek(i[2],0)
                Data = fr.read(i[1])
                fw = open(Path,'wb')
                fw.write(Data)
                fw.close()
        fr.close()

if __name__ == '__main__':
    extract(sys.argv[1])
