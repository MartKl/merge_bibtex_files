# merge bib files from one directory into merged.bib
# in case of duplicate entries it takes the one from the latest file
import glob
import os
#https://stackoverflow.com/questions/21662474/splitti|ng-a-string-with-brackets-using-regular-expression-in-python
import re

bib_folder = './bibfiles/'

# import bibtexparser #has troubles with the month entries
# from pybtex.database import parse_file, BibliographyData, Entry #also troubles

def split_bibtext(bibtext):
    '''Converts a bibtex text into (keys,entries), where entries is a list of the bibtex entries  and keys a list of the keys.
       The "@" in the beginning of entry needs to be the first non-space character of a line.'''
    if '@' not in bibtext:
        return ([],[])
    
    #list of lines of bibtext
    biblist = bibtext.splitlines()
    biblist = list(filter(None, biblist))

    #remove tabs before @
    for j, line in enumerate(biblist):
        biblist[j] = re.sub(r'([ \t]+(?=@))', '', line, flags=re.M)

    #remove everything before the first entry
    j=0
    while (biblist[j][0] != '@') & (j<len(biblist)):
        j +=1
    biblist = biblist[j:]

    entry = []
    entrylist = []
    keys = []
    for j in range(len(biblist)):
        line = biblist[j]
        if line[0]=='@':
            #get key
            try:
                key = re.search('@.*\{(.+?),', line).group(1)
            except AttributeError:
                key = '' # apply your error handling
            #append key and entry, both as string
            keys.append(key)
            entrylist.append( '\n'.join(entry) )
            entry = [line]
        else:
            entry.append(line)
    return (keys,list(filter(None, entrylist)))

# all bib files in folder
file_names = glob.glob(bib_folder+'*.bib') 

#sort from newest to oldest, getmtime needed in windows
file_names.sort(key = os.path.getmtime, reverse=True)

#read bib files ordered from newest to oldest, files saved as lists of tuples (key, bib_entry)
bibtexts = []
key_lists = []
for file_name in file_names:
#     print(file_name)
    file  = open(file_name, 'r', encoding='utf8', errors = 'ignore') 
    file_content = file.read()
    file.close()
    keys, bibtext = split_bibtext( file_content )
    key_lists.append( keys )
    bibtexts.append( bibtext )
        
        
merged_bibtext = bibtexts[0]
merged_keys = key_lists[0]
for keys, bibtext in zip(key_lists[1:], bibtexts[1:]):
    for key, entry in zip(keys,bibtext):
        if key not in merged_keys:
            merged_keys.append(key)
            merged_bibtext.append(entry)
            

file_merged = open('./merged.bib','wb+')
#convert to one string
merged = '\n'.join(merged_bibtext)
file_merged.write(merged.encode('utf8', 'ignore'))
file_merged.close()


print( '{} entries in merged file'.format( len(merged_bibtext) ) )

