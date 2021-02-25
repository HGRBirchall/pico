# checks for existing file and 
import uos

# check if file exists and create a new file if not, or increment the number if it does
class NewFile:
    
    def __init__(self, file_name,j):
        file = file_name
        try:
            while uos.stat(str(file_name)+".txt"):
                print ("File \""+ str(file_name)+ ".txt\" already exist")
                j = int(j)+1
                file_name = file+str(j)
            
        except OSError:
            file_name = str(file_name) + ".txt"
            print ("File has been created as \"" + str(file_name) +"\"")
            j = int(j)+1
