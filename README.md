# README #
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