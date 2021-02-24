# checks for existing file and 
import uos

# check if file exists and create a new file if not, or increment the number if it does
class NewFile:
    
    def __init__(self, file_name,j):
        try:
            while uos.stat(file_name):
                print ("File \""+ str(file_name)+ "\" already exist")
                j = int(j)+1
                file_name = "/data/soil_logger"+str(j)+".txt"
            
        except OSError:
            print ("File has been created as \"" + str(file_name) +"\"")
            j = int(j)+1
