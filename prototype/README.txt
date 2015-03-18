

             ('-.          (`-.      ('-.   ('-.     .-') _     .-')    
            ( OO ).-.    _(OO  )_  _(  OO) ( OO ).-.(  OO) )   ( OO ).  
   .-----.  / . --. /,--(_/   ,. \(,------./ . --. //     '._ (_)---\_) 
  '  .--./  | \-.  \ \   \   /(__/ |  .---'| \-.  \ |'--...__)/    _ |  
  |  |('-..-'-'  |  | \   \ /   /  |  |  .-'-'  |  |'--.  .--'\  :` `.  
 /_) |OO  )\| |_.'  |  \   '   /, (|  '--.\| |_.'  |   |  |    '..`''.) 
 ||  |`-'|  |  .-.  |   \     /__) |  .--' |  .-.  |   |  |   .-._)   \ 
(_'  '--'\  |  | |  |    \   /     |  `---.|  | |  |   |  |   \       / 
   `-----'  `--' `--'     `-'      `------'`--' `--'   `--'    `-----'  


filter.py will output a text file with possible candidates with corrections. Text file is in ISO-8859 standard.
In order to manipulate is in UNIX systems using grep and other commands, one may need to convert it to utf-8 format.
To do this: 

iconv -f iso-8859-1 -t utf-8 file2beconverted.txt > converted_utf8.txt

OR

iconv -f iso-8859-1 -t utf-8 file2beconverted.txt -o file2beconverted.txt    

Above will redirect the output back to the file



 .-') _                             _ .-') _               
(  OO) )                           ( (  OO) )              
/     '._  .-'),-----.              \     .'_  .-'),-----. 
|'--...__)( OO'  .-.  '             ,`'--..._)( OO'  .-.  '
'--.  .--'/   |  | |  |             |  |  \  '/   |  | |  |
   |  |   \_) |  |\|  |             |  |   ' |\_) |  |\|  |
   |  |     \ |  | |  |             |  |   / :  \ |  | |  |
   |  |      `'  '-'  '             |  '--'  /   `'  '-'  '
   `--'        `-----'              `-------'      `-----' 




- Implemented possible duplicate search using Python fuzzy sequence matching. The cutoff margin is hand picked by trial and error.
- Implemented spell corrector. Based on simple permutation technique using a corpus. Current corpus is not rich in IT related terms. But it does a fairly good job. Need to investigate if adding more IT related content to the corpus will improve the corrections. Note that, simply including a corpus with correctly spelled words (from a dictionary for eg.) will not work as we need to include most common misspells of the same words (in some amount) for the algorithm to be unbias.
- Next: 
-- try techniques used in natural language processing (stem word search and simple prediction methods etc.), 
-- summarize possible duplicates/spell corrections in a table (HTML/CSV/JSON?)
-- May be develop a JS a HTML table where user can select what to keep out of duplicates and corrections
