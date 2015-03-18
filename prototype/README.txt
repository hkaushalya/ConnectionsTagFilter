filter.py will output a text file with possible candidates with corrections. Text file is in ISO-8859 standard.
In order to manipulate is in UNIX systems using grep and other commands, one may need to convert it to utf-8 format.
To do this: 

iconv -f iso-8859-1 -t utf-8 file2beconverted.txt > converted_utf8.txt

OR

iconv -f iso-8859-1 -t utf-8 file2beconverted.txt -o file2beconverted.txt    

Above will redirect the output back to the file

