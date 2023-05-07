import os
import time
import shutil
import platform

# update_log() prints the log info and writes it in the log file
def update_log(path, file_name, type, log_file):
    # This try is obsolete, even if I delete the log file, when the program is running
    # open() will create another log file with the same name, but anyway...
    try :
        f = open(log_file, "a")
        if type == 'removed':
            print(path.ljust(20," ") + file_name.ljust(20," ") + type.ljust(10," "))
            f.write(path.ljust(20," ") + file_name.ljust(20," ") + type.ljust(10," ") + "\n")
        else:
            """
            if platform.system() == 'Windows':
                creation_date = os.path.getctime(path + file_name).st_birthtime
            else:
                creation_date = os.path.getctime(path + file_name).st_mtime
            """
            #change the format for creation date
            print(path.ljust(20," ") + file_name.ljust(20," ") + type.ljust(10," "))
            f.write(path.ljust(20," ") + file_name.ljust(20," ") + type.ljust(10," ")+ "\n")
        f.close()
    except FileNotFoundError:
        print("The log file has been deleted\n")
        print("Exiting the program...\n")
        os.exit()


def synchronize(src, dst, log_file):
    
    src_list = os.listdir(src)
    dst_list = os.listdir(dst)

    for src_item in src_list:
        if src_item in dst_list:
            try:
                if os.stat(src + src_item).st_mtime > os.stat(dst + src_item).st_mtime:
                    if os.path.isfile(src + src_item):
                        shutil.copy(src + src_item, dst)
                        update_log(src, src_item, 'updated', log_file)
                        update_log(dst, src_item, 'updated', log_file)
                    elif os.path.isdir(src + src_item):
                        shutil.rmtree(dst + src_item) 
                        shutil.copytree(src + src_item, dst + src_item, copy_function = shutil.copy)                        
                        update_log(src, src_item, 'updated', log_file)
                        update_log(dst, src_item, 'updated', log_file)
            except OSError:
                continue

    for dst_item in dst_list:
        if dst_item not in src_list:
            try :
                if os.path.isfile(dst + dst_item):
                    os.remove(dst + dst_item) 
                    update_log(src, dst_item, 'removed', log_file)
                    update_log(dst, dst_item, 'removed', log_file)
                elif os.path.isdir(dst + dst_item):
                    shutil.rmtree(dst + dst_item) 
                    update_log(src, dst_item, 'removed', log_file)
                    update_log(dst, dst_item, 'removed', log_file)                    

            except OSError:
                update_log(src, dst_item, 'removed', log_file)
                update_log(dst, dst_item, 'removed', log_file)             
                  
    for src_item in src_list:
        if src_item not in dst_list: 
            if os.path.isfile(src + src_item):
                try:
                    shutil.copy(src + src_item, dst)
                    update_log(src, src_item, 'created', log_file)
                    update_log(dst, src_item, 'copied', log_file)
                except OSError:
                    continue
            elif os.path.isdir(src + src_item):
                try:
                    shutil.copytree(src + src_item , dst + src_item, copy_function = shutil.copy)
                    update_log(src, src_item, 'created', log_file)
                    update_log(dst, src_item, 'copied', log_file)
                except OSError:
                    continue


# Gets the source path from the keyboard and checks if it's a valid path
# If it's not a valid path, it asks again for a valid path
# Adds / if needed
path_to_source = input('\t Please enter the path to the source folder: \n')
while not os.path.isdir(path_to_source):
    path_to_source = input('\t Invalid path to folder, please renter the path to the source folder:\n')

format_path = ""
for aux in path_to_source:
    if aux == '\\':
        format_path += '/'
    else:
        format_path += aux
path_to_source = format_path

if path_to_source[-1] != '/':
   path_to_source = path_to_source + '/'

# Gets the replica path from the keyboard and checks if it's a valid path
# If it's not a valid path or the path of replica is the same as the path for source
# It asks again for a valid path
# Adds / if needed
path_to_replica = input('\t Please enter the path to the replica folder: \n')
while (not os.path.isdir(path_to_source)) or (path_to_replica == path_to_source):
    path_to_replica = input('\t Invalid path to folder, please renter the path to the replica folder:\n')

format_path = ""
for aux in path_to_replica:
    if aux == '\\':
        format_path += '/'
    else:
        format_path += aux
path_to_replica = format_path

if path_to_replica[-1] != '/':
    path_to_replica = path_to_replica + '/'

# Gets the interval for synchonization and it ensures that it was given a numeric value
# Then converts the string of digits to int
sync_interval = input('\t Please enter the synchonization interval in seconds: \n')
while not sync_interval.isnumeric():
    sync_interval = input('\t Invalid value, please enter the synchonization interval in seconds: \n')
sync_interval = int(sync_interval)

# Makes sure that the path to the log file is valid and the file is .txt
path_to_log = input('\t Please enter the path to the log file (log file should be .txt): \n')
while (not os.path.isfile(path_to_log)) or (path_to_log [-4:] != '.txt'):
    path_to_log = input('\t Invalid path, please renter the path to the source folder (log file should be .txt):\n')

format_path = ""
for aux in path_to_log:
    if aux == '\\':
        format_path += '/'
    else:
        format_path += aux
path_to_log = format_path



while True :
    synchronize(path_to_source, path_to_replica, path_to_log)
    try:
        print("The program will sleep for " + str(sync_interval)+ " seconds...")
        time.sleep(sync_interval)
    except KeyboardInterrupt:
        print('Exiting the program...')
        break



