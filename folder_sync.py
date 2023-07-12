
import time
import os
import sys
import shutil

def folders_sync(source_folder, replica_folder, interval, log_file):
    
	while True:
		#adds the files/directories in the source and replica folders to a set
		source_content = set(os.listdir(SRC))
		replica_content = set(os.listdir(DEST))

		#checks if there are any new files/directories in the source set to the replica set and adds them to the new_files set
		new_content = source_content - replica_content
		#creates an empty set for files that have been modified
		modified_content = set()
		#compares the source and replica sets to see files in common
		for file in source_content.intersection(replica_content):
			source_path = os.path.join(os.path.realpath(source_folder), file)
			replica_path = os.path.join(os.path.realpath(replica_folder), file)
			#check the modification time to see if the files have been changed and adds them to the modified files set
			if os.path.getmtime(source_path) > os.path.getmtime(replica_path):
				modified_content.add(file)
		
		#checks if there are any different files from the replica set to the source set and adds them to the deleted_files set
		deleted_content = replica_content - source_content
		#checks all of the files in the new_files and the modified files sets
		for file in new_content.union(modified_content):
			source_path = os.path.join(os.path.realpath(source_folder), file)
			replica_path = os.path.join(os.path.realpath(replica_folder), file)
			#copies files from source to replica 
			if os.path.isfile(source_path):
				shutil.copy2(source_path, replica_path)

			#copies directories from source to replica
			elif os.path.isdir(source_path):
				shutil.copytree(source_path, replica_path, dirs_exist_ok=True)
		
		#function that deletes the files that exist in deleted_files set
		for file in deleted_content:
			replica_path = os.path.join(replica_folder, file)
			#removes files
			if os.path.isfile(replica_path):
				os.remove(replica_path)
			#removes directories
			elif os.path.isdir(replica_path):
				shutil.rmtree(replica_path)

		#write information onto a log file
		with open(log_file, 'a') as log:
			log.write(f'{time.ctime()}: Synch Complete\n')
			log.write(f'New files/directories: {", ". join(new_content)}\n')
			log.write(f'Modified files/direcotories: {", ".join(modified_content)}\n')
			log.write(f'Deleted files/directories: {", ".join(deleted_content)}\n\n')
		
		print(f'{time.ctime()}: Synch Complete\n')
		print(f'New files/directories: {", ". join(new_content)}\n')
		print(f'Modified files/directories: {", ".join(modified_content)}\n')
		print(f'Deleted files/directories: {", ".join(deleted_content)}\n\n')
		
		time.sleep(int(interval))

if __name__ == '__main__':

	SRC = input("Insert the name of the source folder: ")
	DEST = input("Insert the name of the replica folder: ")
	interval = input("Set the time inbtween synchronizations in seconds: ")
	log_file = input("Insert the log file: ")

	folders_sync(SRC, DEST, interval, log_file)
