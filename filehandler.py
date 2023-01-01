import os
import rarfile
import zipfile
import shutil



"""This file handles logic for standardizing the content of the http response, it exisits because the repsonse from gambanana
wil be a compressed arquive that can be organized in any way (dirs and subdirs), this will find the file we are looking for
in ay depth"""

#receives a httpResponse and optional path

def extract_bsp(response, outputfolder="./"):
    with open('temp.bin', 'wb') as f: 
        f.write(response.content)
    if rarfile.is_rarfile('temp.bin'):
        rar = rarfile.RarFile('temp.bin')
        for fil in rar.infolist(): # checks fot the bsp in any depth
            if fil.filename.endswith('.bsp'):
                rar.extract(fil.filename, outputfolder)
                os.remove('temp.bin')
                
                # if the bsp was in a folder inside the arquvie it would extract the folder with it, this extracts it from
                # the folder it came from and than deletes the folder
                file_name = os.path.basename(fil.filename)
                parent_dir = os.path.dirname(fil.filename)
                if parent_dir != '':
                    shutil.move(f"{outputfolder}/{parent_dir}/{file_name}", f"{outputfolder}/{file_name}")
                    os.rmdir(f"{outputfolder}/{parent_dir}")


                return os.path.basename(fil.filename)
    elif zipfile.is_zipfile('temp.bin'):
        zi = zipfile.ZipFile('temp.bin')
        for fil in zi.infolist():
            if fil.filename.endswith('.bsp'):
                zi.extract(fil.filename, outputfolder)
                os.remove('temp.bin')
                
                file_name = os.path.basename(fil.filename)
                parent_dir = os.path.dirname(fil.filename)
                if parent_dir != '':
                    shutil.move(f"{outputfolder}/{parent_dir}/{file_name}", f"{outputfolder}/{file_name}")
                    os.rmdir(f"{outputfolder}/{parent_dir}")
                return os.path.basename(fil.filename)
    else: # could modify this to raise an exepton but lol
        os.remove('temp.bin')
        return "0"
    


