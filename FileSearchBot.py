import os, string
import pymongo
from pymongo import MongoClient
import logging
#logging.basicConfig(filename="HelpDesk_Chatbot.log",level=logging.INFO,format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")


def get_connection(uri,db,collection):
    """
    This module
    :param uri:
    :param db:
    :param collection:
    :return:
    """
    try:
        client = MongoClient(uri)
        client.server_info()
        db_connection = client[db][collection]
        return db_connection
    except (pymongo.errors.ServerSelectionTimeoutError) as err:
        logging.info("Connection not established!!")
        return None

def test():
    return 1

# Listing list of drive in system
def list_drive():
    available_drives = ['%s:/' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    return available_drives

def list_directory(path):
    """
    Listing the folders in the directory
    :param drive:
    :return: list of directories
    """
    list_dir = os.listdir(path)
    # Checking the list of directory
    list_dir = [dire for dire in list_dir if os.path.isdir(path+"/"+dire)==True]
    return list_dir

def list_files(path):
    """
    Listing the files in the directory
    :param drive:
    :return: list of files
    """
    print(path)
    files = os.listdir(path)
    print(files)
    # Checking the list of files
    files = [file for file in files if os.path.isfile(path+"/"+file)==True]
    return files

def main(FileDB):
    """

    :param FileDB:
    :return:
    """
    # checking db connection
    db_conn = get_connection(FileDB["file"]["uri"],FileDB["file"]["db"],FileDB["file"]["collection"])
    # if db is not connected
    if db_conn is not None:
        # list all drives
        drive_list = list_drive()
        # Iterating over drive
        for drive in drive_list:
            # walk through the root directory

            for root, directories, filenames in os.walk(drive):
                # iterating files
                data_list = []
                for filename in filenames:
                    data = {"path":root.replace("\\","/"),"file":filename}
                    # storing in db
                    data_list = data_list + [data]
                # insert many
                try:
                    db_conn.insert_many(data_list)
                except:
                    pass
    else:
        print("DB error")
    return drive_list

def search_file(file_name):
    """

    :param file: File_Listing.py
    :return:
    """
    search_file = file_name.lower()
    # list all drives
    drive_list = list_drive()
    # Iterating over drive
    for drive in drive_list:
        # walk through the root directory
        for root, directories, filenames in os.walk(drive):
            filenames = [files.lower() for files in filenames]
            if search_file in filenames:
                return root.replace("\\","/")

if __name__ == '__main__':
    logging.info("Start")
    FileDB = {"file": {"uri": "mongodb://localhost:27017", "db": "FileBot", "collection": "files"}}
    #main(FileDB)
    file_name = "FileSearchBot.py"
    logging.info("Search File : "+ file_name)
    logging.info("File location : "+ search_file(file_name))
    logging.info("End")
    #print(main())
    #print(list_drive())
    #print(list_directory())
    #print(list_files("D:"))
