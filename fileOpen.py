#Code by Faizan Ahmed & M. Deedahwar.
#Copyrights 2020.

#import statements
from sys import getsizeof
from _collections import deque
import threading
from _thread import start_new_thread

from socket import *



#declare global variables

global threading_file
global threading_number
global op
global files_output
global output_file
global files_input

#initializing the necesary variables

systemSize = 1000
SystemSectorSize = 100
start = []
end = []
systemFile = ""
file_in_action = ""
files_accessed = []
mode = ""
database = [0]
username = ''

host = ''
port = 1234

files_output = ["outthread1.txt","outthread2.txt","outthread3.txt","outthread4.txt","outthread5.txt"]
files_input = ["inthread1.txt","inthread2.txt","inThread3.txt","inthread4.txt","inthread5.txt"]


# to show if the user file is available in the database or not
file_available = False

#initializing stacks with deque
filled_sectors = deque()
available_sectors = deque()
available_sectors.append(0)

#ceating database
#class constructors
class Node:
    def __init__(self, filename =None, start_value=None, end_value=None, file_size= 0):
        self.start_value = start_value
        self.end_value = end_value
        self.filename = filename
        self.next_value = None
        self.file_size = 0 

class SLinkedList:
    def __init__(self):
        self.head_value = None
        self.tail_value = None
        self.file_size = 0  # for maintaining file size and using in read/write operations

                                         #################### MENU #####################



def menu(option):
    if option == 0:   #select option 0 to quit
        quitprogram()
        
    elif option == 1: #select option 1 to create a file
        create("")
    elif option == 2: #select option 2 to open a file
        openFile()
    elif option == 3: #select option 3 to close a file
        closeFile()
    elif option == 4: #select option 4 to write in a file
        writeFile()
    elif option == 5: #select option 5 to read from a file
        readFile()
    elif option == 6: #select option 6 to delete a file
        delete()
    elif option == 7: #select option 7 to map the memory
        memoryMap()
    else:             #incase an invalid option is selected
        print("Invalid option!")
        
                                         ###############################################

#To exit the program. 
def quitprogram():
        exit()
        systemFile.close()
        global start
        start = []
        global end
        end = []

# to create a binary system file
def system_file():
    global systemSize
    #opening sys.txt file
    f = open('sys.txt', 'wb')
    f.seek(systemSize-1)
    f.write(b"\0")
    #closing sys.txt file
    f.close()

# to get the available space
def spaceAvailable():
    #increasing the scope of the variables
    global systemSize
    global SystemSectorSize
    global available_sectors
    #setting the size of the sector
    sector_size = SystemSectorSize
    #calculating sector number to determine iterations
    sector_number = systemSize/sector_size
    #looping on the sectors
    while sector_number-1 != 0:
        available_sectors.append(sector_size+1)
        sector_size = sector_size+100
        sector_number = sector_number-1

#to locate the file
def locate_file(name):
    #increasing scope
    global start
    global end
    #looping on the items in our database to locate the required file
    for item in database:
        if item == 0:
            print()
        elif item.head_value.filename == name:
            #extracting values from all nodes of file
            current_place = item.head_value
            while current_place is not None:
                start.append(current_place.start_value)
                end.append(current_place.end_value)
                current_place = current_place.next_value

#writing new sector
def write_new_sector(data):
    global output_file
    remaining_data = data
    remaining_data_size = len(remaining_data.encode('utf-8'))
    if available_sectors:
        next_available_sector = available_sectors.pop()
        filled_sectors.append(next_available_sector)
        systemFile.seek(next_available_sector)
        #moving to the points where data is to be written.
        systemFile.write(remaining_data)

   
    else:
        #print("System is out of space. Please delete some files to make space.")
        file = open(output_file, "a")
        file.write("Insufficient space in the system, delete some files first!" )

    for item in database:
        if item==0:
            file = open(output_file, "a")
            file.write("Error! No item found\n")
        if file_in_action == item.head_value.filename:
            new_log = Node(start_value=next_available_sector, end_value=next_available_sector + remaining_data_size)
            item.tail_value.next = new_log
            item.tail_value = new_log
        #print("Written successfully ", file_in_action)
            file = open(output_file, "a")
            file.write("Data write was successful!" )


#appending within a sector
def within_sector_append(occupied_sector_space, write_data, remaining_sector_space, s):
    #moving file pointer to the point from where we can start appending
    systemFile.seek(s + occupied_sector_space)
    #writing only the data that can fit in remaining space
    data_to_write = write_data[:remaining_sector_space]  
    systemFile.write(data_to_write)
    systemFile.seek(0)

#updating file size in the database
def update_file_size(update_file, new_size):
    for file in database:
        if file.head_value.filename == update_file:
            file.head_value.file_size = new_size

    return 0


#function to create a file
def create(file_name):
    global file_available
    global output_file
    if file_name == "":
        #getting the name of the file
        #file_name = input("Enter your file name: ")
        file_name = (op[1])
        create(file_name)
        #checking if file is too big
        while len(file_name.encode('utf-8')) > 50:
            file_name = input("File name too big.\n Try again(Less than 50 chars): ")
    #checking for sectors
    file = open(output_file, "a")
    if available_sectors:   
        sector_in_use = available_sectors.pop()
        space_starting = sector_in_use
        space_ending = space_starting+(SystemSectorSize-1)
        #creating file sector in the sysfile
        filled_sectors.append(sector_in_use)
        #print("Creating...")
        new_list = SLinkedList()
        new_head_entry = Node(filename=file_name, start_value=space_starting, end_value=space_ending)
        new_list.head_value = new_head_entry
        new_list.tail_value = new_head_entry
        #adding list to the database array
        database.append(new_list)                    
        #writing to output file.
        file.write("File: " + file_name + " : Created Successfully\n")
    else:
        file.write("Insufficient space, Please delete a few files.")
        #"Your system is out of space. Please delete a file to make space.")


    status = "created"
    return status


#to open a file
def openFile():
    #increasing the scope
    global file_in_action
    global mode
    global systemFile
    global file_size
    global output_file
    
    #getting the file name and the mode i.e. to read or to write or to append
    file_in_action = op[1]
    mode = op[2]
    systemFile = open("sys.txt", mode)
    locate_file(file_in_action)

    #finding file size to store in global variable
    for file in database:
        if file == 0:
            continue
        if file.head_value.filename == file_in_action:
            file_size = file.file_size

    file = open(output_file,"a")
    file.write("File: "+ file_in_action + " : has been opened\n")

    status = "opened"

    return status

# to close the file
def closeFile():
    global output_file
    response = op[1]
    file = open("sys.txt", "w")
    file.seek(0)
    file.close()

    file = open(output_file,"a")
    file.write(response + " : file has been closed.\n")
    status = "closed"
    return status

#to read a file
def readFile():
    global start
    global end
    global systemFile
    global mode
    global output_file
    a = 0
    b = 0
    data = ""
    
    mode = op[2]
    file = open(output_file, "a")
    if mode == "r":
        systemFile = open("sys.txt", mode)
        for item in database:
            if item == 0:
                print("")
            elif item.head_value.filename == file_in_action:
                print("File has been fetched. ")
                next_segment = item.head_value
                while next_segment is not None:
                    beginning = next_segment.start_value
                    ending = next_segment.end_value
                    size_of_segment = ending - beginning
                    systemFile.seek(beginning)
                    data = systemFile.read(size_of_segment)
                    next_segment = next_segment.next_value
        file.write("Data from file "+ file_in_action+ " :" + data+ "\n")
    else:
        file.write("Error! Open in mode r")
    return data
                    
   


def writeFile():
    #Globalizing variables
    global start
    global end
    global mode
    global file_in_action 
    global systemFile
    global output_file

    mode = op[2]

    systemFile = open("sys.txt", mode)
    

    new_file_size = 0 #Set the file size to 0

    #Take input of content to be written
    
    write_data = op[3]
    write_data_size = len(write_data.encode('utf-8')) 

    new_file_size = new_file_size+write_data_size #Set new file size
        
    locate_file(file_in_action) #call function locate_file

    #for append mode

    if mode == "a":
        size = len(start) #Calculate size
        #Set start and end points
        start_point = start[size-1]   
        end_point = end[size-1]    
        systemFile.seek(start_point-1)
        readingSystemFile = open("sys.txt", "r")
        occupied_sector_space = len(readingSystemFile.read(100))
        remaining_sector_space = 99 - occupied_sector_space
        if occupied_sector_space < 100: #If file space is greater than 100
            if write_data_size > remaining_sector_space:
                within_sector_append(occupied_sector_space, write_data, remaining_sector_space, start_point)
                remaining_data = write_data[remaining_sector_space:]
                write_new_sector(remaining_data)     
            else:    
                within_sector_append(occupied_sector_space, write_data, remaining_sector_space, start_point)
        elif occupied_sector_space == 100:
            write_new_sector(write_data)

    # write mode
    if mode == "w":
        new_file_size = write_data_size  # because all data will be overwritten by this data
        deleteFile(file_in_action)
        create(file_in_action)
        size_available = end[0]-start[0]

        if write_data_size < size_available:
            within_sector_append(0,write_data,size_available,start[0])
        else:    # write_data_size > size_available:
            within_sector_append(0, write_data, size_available, start[0])
            remaining_data = write_data[size_available:]
            write_new_sector(remaining_data)
    #print("Succesfully written")
    file = open(output_file, "a")
    file.write = ("Updated Successfully.")
    #file_in_action.head_value.file_size = new_file_size

    #update_file_size(file_in_action, new_file_size)


# to delete the file

def delete():
    global output_file
    delFile = op[1]
    deleteFile(delFile)
    file = open(output_file, "a")
    file.write("File "+delFile+" : Successfully deleted\n")

    
def deleteFile(delete_file):
    
    locate_file(delete_file)
    global start       # using file start points from array start
    for file in database:
        if file == 0:
            print()
        elif file.head_value.filename == delete_file:
            space = file.head_value
            while space is not None:     # removing starting points from filled sector deque so they're available again
                start_point = space.start_value
                filled_sectors.remove(start_point)
                available_sectors.append(start_point)
                space = space.next_value
            # removing file log from DB
            database.remove(file)

    print("File deleted successfully!")  #assuring the user

    # removing actual data is yet to be figured out :(
    status = "deleted"
    return status


def memoryMap():
    global output_file
    file = open( output_file, "a")
    
    for file in database:
        if file == 0:
            print("FILE\tSIZE")
        else:
            print("working.....")
            name = file.head_value.filename
            size = file.head_value.file_size
            print(name, "\t", size)
            file.write(name + "\t" + str(size)+ "\n")
            mapp = str(name + "\t" + str(size)+ "\n")
    #print(database)
    return mapp

def file_check():
    global files_accessed
    global file_in_action
    global username
    for item in files_accessed:
        if item[0] == file_in_action:
            if item[1] == 5:
                message = "File has been accessed the max 5 times"
                return message
            if len(item) == 5:
                if (item[2] != username) or (item[3] != username) or (item[4] != username):
                    message = "File can not accomodate more users"
                    return message
                else:
                    item[1] += 1
                    message = "access granted"
                    return message
                    
            
            item[1] += 1
            item.append(username)
            message = "access granted"
            return message
        
    files_accessed.append([file_in_action, 1, username])
    message = "access granted"
    return message
        
            
    



def server_thread(conn):
    global mode
    global op
    global file_in_action
    global username
    
    username=conn.recv(100).decode()
    if username.startswith("username"):
        print(username)
        conn.send(( "\nFile Management System\n 1.Open File\n 2.Create File\n 3.Read File\n 4.Write to File\n 5.Delete File\n 6.Close file\n 7.Show Memory Map\n 8.Logout").encode())
    while True:
        
        msg = conn.recv(1024).decode()
        #if (msg.startswith("option")):
        op = msg.split(' ', 3)
        
        print(op)
        
        choice = op[0]
        if (choice == '8'):
            
            conn.close()
            execute_server()
            
        file_in_action = op[1]
        if (file_in_action != '') or (file_in_action != ' '):
            access = file_check()
            print(access)
            if access != "access granted":
                conn.send(access.encode())
                continue
                
            
        #mode = op[2]
        #data = op[3]
        if (choice == '1'):
            
            
            openFile()
            msg = file_in_action + ' opened successfully in ' + mode + " mode";
            print(msg)
            conn.send(msg.encode())
        if (choice == '2'):
            
            status = create('')
            msg = status
            print(msg)
            conn.send(msg.encode())
        if (choice == '3'):
            mode = "r"
            data = readFile()
            msg = file_in_action + ' read succesfully with data: ' + data
            print(msg)
            conn.send(msg.encode())
        if (choice == '4'):
            
            
            data = op[3]
            writeFile()
            msg = data + " succesfully written on " + file_in_action
            print(msg)
            conn.send(msg.encode())
        if (choice == '5'):
            
            delete()
            msg = file_in_action + " deleted successfully"
            print(msg)
            conn.send(msg.encode())
        if (choice == '6'):
            
            closeFile()
            msg = file_in_action + " closed successfully"
            print(msg)
            conn.send(msg.encode())
        if (choice == '7'):
            mem_map = memoryMap()
            conn.send(mem_map.encode())




def execute_server():
    global threading_file
    global threading_number
    global op
    global files_output
    global output_file
    global files_input
    global mode
    global file_in_action
    global username
    global files_accessed
    global file_available
    global systemSize
    global SystemSectiorSize
    global host
    global port
    global conn
    

    
    


    if __name__ == '__main__':
        threads = 0
        spaceAvailable()
        system_file()
        #print("\nWelcome" )
        server_socket = socket(AF_INET, SOCK_STREAM)
        try:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind((host, port))
        except error as e:
            print(str(e))

        print("active server")
        server_socket.listen(10)
        while True:
            conn, addr = server_socket.accept()
            print("server connected to " + addr[0] + ":" + str(addr[1]))
            start_new_thread(server_thread, (conn,))
            threads += 1
            output_file = files_output[threads]
            print('Thread Number: ' + str(threads))


execute_server()
        
    
        




    
