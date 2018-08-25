# MergeBibFiles -- A simple way to merge bibtex files

## A simple tool for a simple but common task

*Author:* [Martin Kliesch](http://www.mkliesch.eu/)

*Preparation: copy bibtex files (file ending "bib") into the subfolder "./bibfiles/"

*Output: It generates a new file "merged.bib" with all bibtex entries from those bibtex files. In case of multiple entry keys, it takes the one from the most recent file. 

* Needs: glob, os, re

