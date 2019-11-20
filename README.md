# randword
Random Word Generator

### Requirements
At least one dictionary and affix file are required.

Dictionaries in iSpell/MySpell/Hunspell format will work.

Affix files need to be in the MySpell/Hunspell format; handling for iSpell format files may be included later.

### Using the utility
Usage `randword.py [number of words] -d [delimiter]` OR `randword.py [number of words] --delim [delimiter]`  

Output the specified number of words to stdout.

The default delimiter is a single space.

### Configuration
The path and name for the dictionary/affix files are defined near the start of the file and can be changed if required.

The default number of words is also configurable from the same location.

It is also possible to set a list of the affixes which will be ignored, using the EXCLUDE_AFFIXES setting.
The affixes can be included in a single string, as this is built into a set when the program runs.

### KNOWN BUGS
None at present

### Future plans for development

Add the ability to specify the dictionary and affix file on the comamnd line
