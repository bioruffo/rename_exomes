#!/usr/bin/env python3

'''
This script will rename .bam, .bai, .vcf(.gz) and .vcf(.gz).tbi files according
to their barcode.
Usage:
1)  Save a list of names and barcodes in a file called "samples.txt",
    in the form:
        name <tab> number
    i.e. if the sample "John Doe" corresponds to barcode IonXpress_003, save
    this text as samples.txt:
        John_Doe <tab> 3
2)  Copy the directory name to your clipboard
3)  Execute the rename_exomes.py file.


'''



# Import modules
import os
from tkinter import Tk, messagebox

SKIP_TOKEN = 'SKIP'

# Get text from the clipboard
try:
    paste = Tk().clipboard_get()
except Exception as exc:
    messagebox.showwarning('Warning', 'No valid data found in clipboard.')
else:
    try:
        
        # Get the file list from the directory
        walk = os.walk(paste)
        files = list(walk)[0][2]
    except:
        messagebox.showwarning('Warning', 'No valid directory found in clipboard.')
    else:
        samplesfile = os.path.join(os.path.normpath(paste), 'samples.txt')
        try:
            with open(samplesfile, 'r') as samplesfile:
                samples = [sample.strip().split('\t') for sample in samplesfile.readlines()]
        except FileNotFoundError:
            messagebox.showwarning('Warning', 'No "samples.txt" file found at: ' + paste)
        else:
            renames = dict([(samplename, []) for samplename, barcode in samples])
            
            for samplename, barcode in samples:
                barcode = 'IonXpress_'+barcode.rjust(3, '0')
                for filename in files:
                    if barcode in filename:
                        
                        # Identify all known file types to be renamed
                        for nameend in ['.bam', '.bam.bai']:
                            if filename.endswith(nameend):
                                newname = samplename+nameend
                        for nameend in ['.vcf.gz', '.vcf.gz.tbi']:
                            if filename.endswith(nameend):
                                newname = samplename +'_'+''.join([part.strip('_') for part in filename.split(barcode)])
                                
                        # ...unless the new name already exists; in this case, do not rename this file
                        if newname in files:
                            messagebox.showwarning('Warning', 'File {0} already exists.'.format(newname))
                            renames[samplename].append(SKIP_TOKEN)
                        else:
                            renames[samplename].append((filename, newname))
            
            # Perform the renaming operations
            for samplename, data in renames.items():
                if SKIP_TOKEN in data:
                    continue
                else:
                    for oldname, newname in data:
                        try:
                            os.rename(os.path.normpath(paste+'\\'+oldname), \
                                      os.path.normpath(paste+'\\'+newname))
                        except Exception as exc:
                            messagebox.showwarning('Warning', 'Unable to rename file: {0}.\n{1}'.format(newname, exc))
                            break
print("Script execution complete.")