# BinLister

### SYNOPSIS
  List deleted files from Recycle Bin
  

### DESCRIPTION

 Prior to Windows 7/Vista, a file INFO2 in a hidden directory was used to describe the original files,size and 
 fullpath/name of a deleted file.
 In latests OS versions, this has changed a bit:
 - The hidden Recycle Bin file is located at \$Recycle.Bin\%SID%
 - Two files are created when deleting a file: (e.g: Mypicture.png)
   
   - **$R files** (e.g: $IZY3HAU.png): Contains the file content.
   - **$I files** (e.g: $RZY3HAU.png): Contains the file information (original path/name, size and date of deletion). 
    All $I files are 544 bytes long
  
  In order to list all files an retrieve the proper information from each one (instead of the $I/$R files), we
  can read the $I file structure which is always the same:
  
  -  Bytes 0-7      >	  File Header	 >          Always = 1
  -  Bytes 8-15	    >	  Original file size	 >   Little-endian (HEX)
  -  Bytes 16-23	  >	  Date of file deletion	 >  Number of seconds since January 1, 1601. 
  -  Bytes 24-253	  >	  Original file path	 >  String

 

### ROADMAP

 - [ ] Add Arguments for selecting output folder location
 - [ ] Investigate and leverage "Deleted files permanently" from Recycle Bin



### PARAMETERS 

    -TBD 


### NOTES

  - Version:        0.0.5
  - Author:         polim0rf
  - Creation Date:  16.10.2018
  - Purpose/Change: Initial script development
  - Inspired/adapted from [jtmoran script](https://github.com/jtmoran/recbin)


### EXAMPLES

 * Just run the script and check the /Output folder created.
