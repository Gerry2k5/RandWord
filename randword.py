#!/usr/bin/env python3

import argparse
import mmap
import os
import random
import re
import sys

def main():
    dict_name = "en_GB-large"
    dict_path = "/usr/share/myspell/dicts/"
    
    dict_file = dict_path + dict_name + ".dic"
    affix_file = dict_path + dict_name + ".aff"
    
    default_delim = " "
    default_ignore = "M"

    parser = argparse.ArgumentParser(description="Random Word Generator")
    parser.add_argument(
            "numwords",
            nargs="?",
            type=int,
            default=1,
            help="Number of words to display"
    )
    parser.add_argument(
            "-d", "--delim",
            nargs="?",
            const="",
            default=default_delim,
            help="Delimiter between words (Defaults to a single space)"
    )
    parser.add_argument(
            "-i", "--ignore",
            nargs="?",
            const="",
            default=default_ignore,
            help="Affix(es) to ignore (Defaults to " + default_ignore + ")"
    )
    args = parser.parse_args()

    # TODO: Add args for changing the dictionary and affix file on invocation
    all_affix_rules = get_affix_rules(affix_file)
    wordform_rules = get_words(dict_file, args.numwords)
    
    wordlists = []
    
    affix_ignore_list = set(args.ignore)
    
    for wordform_rule in wordform_rules:
        word_affix_rules = [
                all_affix_rules[affix]
                for affix in tuple(wordform_rule[2])
                if affix not in affix_ignore_list
        ]
        wordlist = apply_affixes(wordform_rule[0], word_affix_rules)
        wordlists.append(wordlist)

    words = [random.choice(wordlist) for wordlist in wordlists]
    # Alternative to above line for testing (will output every word)
#    words = []
#    [words.extend(wordlist) for wordlist in wordlists]

    print(args.delim.join(words))
    

def apply_affixes(base_word, affix_rules):
    """
    Build all possible words by applying affix rules to a base word
    
    Parameters:
    base_word (string):  Base word without any affix specifiers
    affix_rules (list):  Affix rules to be applied
    
    Returns:
    List object containing all words formed by applying
    affixes to the base word.
    """

    # Begin with base word in partial
    # Apply standalone suffixes to base word and add to complete
    # Apply standalone prefixes to base word and add to complete
    # Apply mixable suffixes to base word and add to partial
    # Apply mixable prefixes to partial
    # Add partial to complete
    
    # TODO: Test if it is quicker to add prefixes before suffixes

    complete_words = []
    partial_words = []
    
    partial_words.append(base_word)
    
    complete_words.extend([
            apply_suffix(base_word, affix_rule[3:])
            for affix_rule in affix_rules
            if affix_rule[0] == "SFX" and not affix_rule[1]
    ])
    complete_words.extend([
            apply_prefix(base_word, affix_rule[3:])
            for affix_rule in affix_rules
            if affix_rule[0] == "PFX" and not affix_rule[1]
    ])
    partial_words.extend([
            apply_suffix(base_word, affix_rule[3:])
            for affix_rule in affix_rules
            if affix_rule[0] == "SFX" and affix_rule[1]
    ])
    for partial_word in partial_words[:]:
        partial_words.extend([
                apply_prefix(partial_word, affix_rule[3:])
                for affix_rule in affix_rules
                if affix_rule[0] == "PFX" and affix_rule[1]
        ])
    complete_words.extend(partial_words)
    
    return complete_words


def apply_prefix(base_word, prefix_rules):
    """
    Evaluate prefix rules and apply the relevant rule to a word
    
    Parameters:
    base_word (string):    Base word
    prefix_rules (list):   Prefix rules to be evaluated
    
    Returns:
    The base word with the relevant prefix prepended
    """
    for prefix_rule in prefix_rules:
        if not re.search(prefix_rule[2], base_word):
            continue
        delete_chars = prefix_rule[0]
        prefix_chars = prefix_rule[1]
        part_word = (
                base_word[len(delete_chars):]
                if len(delete_chars) > 0
                else base_word
        )
        break
    else:
        return base_word
    return prefix_chars + part_word
        

def apply_suffix(base_word, suffix_rules):
    """
    Evaluate suffix rules and apply the relevant rule to a word
    
    Parameters:
    base_word (string):    Base word
    suffix_rules (list):   Suffix rules to be evaluated
    
    Returns:
    The base word with the relevant suffix appended
    """
    for suffix_rule in suffix_rules:
        if not re.search(suffix_rule[2], base_word):
            continue
        delete_chars = suffix_rule[0]
        suffix_chars = suffix_rule[1]
        part_word = (
                base_word[:-(len(delete_chars))]
                if len(delete_chars) > 0
                else base_word
        )
        break
    else:
        return base_word
    return part_word + suffix_chars
    

def get_affix_rules(affix_file):
    """
    Read affix rules from a specified file and return these
    in a structured format
    
    Parameters:
    affix_file (string):  Path to affix file
    
    Returns:
    Dict object with the following structure:
        Key:    Identifying letter for this affix
        Value:  List object containing the following objects:
                    [0]: String object containing the value "PFX" or
                         "SFX" to indicate the affix type
                    [1]: Boolean object indicating whether this affix
                         can be combined with other affixes 
                         (only 1 prefix and 1 suffix can be added to
                          a base word)
                    [2]: Integer object indicating how many match rules
                         exist for this affix
                    [3]: 1 or more tuple objects containing the match
                         rules, as follows:
                         [0]: Any letter(s) to be removed from the word
                              (Remove from start of word for prefixes
                               and from end for suffixes, although
                               prefixes do not generally require any
                               removal)
                         [1]: Letters to be added to the word for this
                              rule
                              (Add to start for prefix, add to end for
                               suffix)
                         [2]: Regex expression to be matched for this
                              rule
    """
    rule_dict = {}
    file_open = False
    try:
        with open(affix_file, "r") as f:
            file_open = True
            rule_count = 0
            for line in f:
                if not re.match("^[PS]FX\s", line):
                    continue
                else:
                    rule_data = line.split()
                    if rule_count == 0:
                        rule_type = rule_data[0]
                        rule_id = rule_data[1]
                        can_combine = (
                                True
                                if rule_data[2] == "Y"
                                else False
                        )
                        rule_count = int(rule_data[3])
                        rule_dict[rule_id] = [
                                rule_type, 
                                can_combine, 
                                rule_count
                        ]
                    else:
                        rule_id = rule_data[1]
                        rule_data[2] = (
                                ''
                                if rule_data[2] == "0"
                                else rule_data[2]
                        )
                        rule_data[4] = (
                                "^" + rule_data[4][:]
                                if rule_type == "PFX"
                                else rule_data[4][:] + "$"
                        )
                        rule_dict[rule_id].append(tuple(rule_data[2:]))
                        rule_count -= 1
                
    except OSError:
        error_type = "reading" if file_open else "opening"
        print(
                "Error "
                + error_type
                + " affix file "
                + affix_file, 
                file=sys.stderr
        )
        
    return rule_dict


def get_words(dictionary_file, num_words):
    """
    Get a specified number of words from a dictionary file
    
    Parameters:
    dictionary_file (string):    Path to dictionary file
    num_words (int):             Number of words to be returned
    
    Returns:
    A list of tuples, each of which is obtained by applying
    the str.partition("/") function to each line read from
    the dictionary file
    """
    words = []
    # Outer loop in case of exception
    while len(words) < num_words:
        try:
            with open(dictionary_file, "rb") as f:
                mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
                while len(words) < num_words:
                    word_binary = b''
                    while word_binary == b'':
                        random_pos = int(random.random()
                                         * os.path.getsize(dictionary_file)
                                     )
                        mm.seek(random_pos)
                        mm.readline()   # Move to next line
                        word_binary = mm.readline()
                    word_string = str(word_binary, "utf-8").rstrip()
                    word_form = word_string.partition("/")
                    words.append(word_form)
                    
                mm.close()
            return words
                    
        except OSError:
            print(
                    "Error opening " + dictionary_file + " for reading", 
                    file=sys.stderr
            )
            return None
        
        except ValueError:
            mm.close()
            print(
                    "Seek error at position " + random_pos
                    + " in dictionary file " + dictionary_file, 
                    file=sys.stderr
            )
            

if __name__ == "__main__":
    main()
