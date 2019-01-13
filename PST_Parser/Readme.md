# PST_Parser.py

### SYNOPSIS
  Parses data from PST/OST files (Pff, Personal Folder Files)
  

### DESCRIPTION

 Adapted from the Digital Forensics Cookbook, this script aims to retrieve information from Microsoft PST/OST files leveraging Python libpff/pypff
libraries/wrappers.  
 

### ROADMAP

 - [ ] Tune-up Headers parser
 - [ ] Add attachments parser (Currently not available as a Python binding for libyal/libpff)



### PARAMETERS 

    -pff : indicates the pff file (PST/OST) to be analyzed
    -outputcsv : indicates the location of the CSV output file


### NOTES

  - Version:        1.0.5
  - Author:         polim0rf
  - Creation Date:  19.11.2018
  - Purpose/Change: Initial script development


### EXAMPLES

 * Just run the script and check the /Output folder created.
   - Python PST_Parser.py -pff <location_of_pff_file>
