# randword
Random Word Generator

### Requirements
- At least one dictionary and affix file are required.
- Dictionaries in iSpell/MySpell/Hunspell format will work.
- Affix files need to be in the MySpell/Hunspell format; handling for iSpell format files may be included later.

### Using the utility
Usage:
```randword.py [-h] [-d [DELIM]] [-i [IGNORE]] [--dictfile [DICTFILE]] [--affixfile [AFFIXFILE]] [numwords]
positional arguments:
  numwords              Number of words to display

optional arguments:
  -h, --help            show this help message and exit
  -d [DELIM], --delim [DELIM]
                        Delimiter between words (Defaults to a single space)
  -i [IGNORE], --ignore [IGNORE]
                        Affix(es) to ignore (Defaults to M)
  --dictfile [DICTFILE]
                        Dictionary file to use for word selection
  --affixfile [AFFIXFILE]
                        Affix file to use for generating word variants
```
- The default delimiter is a single space.
- Outputs the specified number of words to stdout.

### Configuration
- The path and name for the dictionary/affix files are defined near the start of the file and can be changed if required.
- The default number of words is also configurable from the same location.
- It is also possible to set a list of the affixes which will be ignored, using the EXCLUDE_AFFIXES setting.
The affixes can be included in a single string, as this is built into a set when the program runs.

### KNOWN BUGS
- None at present

### Future plans for development
- Add the ability to specify the dictionary and affix file on the comamnd line
