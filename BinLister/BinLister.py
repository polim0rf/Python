import winreg
import os
import datetime
import glob
import win32api
import csv


def driveMap():    
	
	# Map all drives in Computer
	drives = win32api.GetLogicalDriveStrings()
	drives = drives.split('\000')[:-1]
	print("[*] Listing all drives in computer:")
	print("\r")
	for drive in drives:
		print("    " + drive)
	return  drives


def returnBinDir(letter):
	
	# Find Recycle.Bin directory
	dirs=[letter + '\Recycler\\',letter + '\Recycled\\',letter + '\$Recycle.Bin\\']
	for recycleDir in dirs:
			if os.path.isdir(recycleDir):
					return recycleDir


def sid_to_user(sid):

	# Map sid to username
	try:
		Key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList" + '\\' + sid)
		(value, type) = winreg.QueryValueEx(Key, r'ProfileImagePath')
		user = value.split('\\')[-1]
		return user
	except:
		return sid


def findRecycled(recycleDir,outfolder):
	
	# List sid's for each drive
	sidlist = os.listdir(recycleDir)
	
	csvcontent=[]
	header = "Drive, $I_file, Deleted_Time, Original_location, Size(Bytes)"
	csvcontent.append(header)
	
	# Iterate through sid's and their $I files
	for sid in sidlist:
		
		try:
			files = os.listdir(recycleDir + sid)
		except:
			continue
		
		user = sid_to_user(sid)
		letter = recycleDir.split("\\",1)[0]
		csvpath = outfolder + "Output_" + "_" + sid + "__" + user + ".csv"
		
		print("\n[*] Listing Recycle.Bin Files For User: " + str(user) + " in " + letter + " drive.")
		
		directory = recycleDir + sid 
		os.chdir(directory)
		fileList = []
		
		# Get list of $I files in directory
		for I in glob.glob("$I*"):
			fileList.append(directory + "\\" + I)	

		if(len(fileList) < 1):
			print("\n    No $I files found in '" + directory + "'")
		else:
			print("\n    (" + str(len(fileList)) + ") $I files found in '" + directory + "'\n")
			print("    File                Date\\Time Deleted          Original Path  (Original Size)")
			print("    ----                -----------------           -----------------------------")
			
			# Prepare file headers
			os.chdir(outfolder)
			if not os.path.isfile(csvpath):
				header = "Drive, $I_file, Deleted_Time, Original_location, Size(Bytes)"
				csvcontent.append(header)
		
		# Read each file, create a row and append
		for f in fileList:
			export = readI(f,letter)	
			csvcontent.append(export)
		
		# Export appended data
		exportCSV(csvcontent,csvpath)		
		csvcontent=[]


def readI(fname,letter):
	
    # Open file and read into 'data'
	export=""
	I = open(fname, "rb")
	data = I.read()
    
    # Read $I FILETIME obj at bytes 16-23 ## http://sunshine2k.blogspot.com/2014/08/where-does-116444736000000000-come-from.html
	date = datetime.datetime.utcfromtimestamp(((int.from_bytes(data[16:24], byteorder='little') - 116444736000000000) / 10000000)).strftime('%H:%M:%S %m/%d/%Y')
    
    # Read original file name at bytes 24+ (26+ to remove trashy characters)
	filename = data[26:]
	filename = filename.decode("utf16").rstrip('\0')
    
	# Read original file size at bytes 8-15
	filesize = int.from_bytes(data[8:16], byteorder='little')

	basename = os.path.basename(fname)
	date = date  + " GMT"
	print("    " + basename.ljust(20) + date.ljust(28) + filename + "  (" + str(filesize) + " bytes)")
	export = (letter  + "," + basename + "," + date + "," + filename.lstrip('\0') + "," + str(filesize))#.encode('utf-8')
	return export


def exportCSV(csvcontent,csvpath):
	
	# Export results in CSV file
	with open(csvpath, "a", newline='', encoding='utf-8-sig') as f:
		writer = csv.writer(f, delimiter=',')
		for val in csvcontent:
			#print(val)
			writer.writerow([val])   
	
			
def main():
	
	# Drive mapping
	drives = driveMap()
	
	# Initialize output folder
	outfolder = os.getcwd() + "\\Output\\"
	if not os.path.exists(outfolder):
		os.makedirs(outfolder)
	
	# Process deleted files
	for drive in drives:
		recycledDir = returnBinDir(drive)
		findRecycled(recycledDir,outfolder)
		
		
if __name__ == '__main__':
	main()
