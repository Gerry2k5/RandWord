#!/usr/bin/env python3

import timeit
from src import randword

REPS=10000
WORD_COUNT=1000

def main():
#    mmap_testing()
#    affix_testing()
    difference_testing()

def affix_testing():
    suffix_first = timeit.Timer(stmt='affix_test(wordform_rules, all_affix_rules)', setup='wordform_rules, all_affix_rules = affix_setup(WORD_COUNT)', globals=globals())
    prefix_first = timeit.Timer(stmt='affix_test_2(wordform_rules, all_affix_rules)', setup='wordform_rules, all_affix_rules = affix_setup(WORD_COUNT)', globals=globals())

    print("With suffixes first, {} repetitions with {} words took {} seconds".format(REPS, WORD_COUNT, suffix_first.timeit(REPS)))
    print("With prefixes first, {} repetitions with {} words took {} seconds".format(REPS, WORD_COUNT, prefix_first.timeit(REPS)))


def difference_testing():
    difference = timeit.Timer(stmt='difference_test_difference(wordform_rules, all_affix_rules)', setup='wordform_rules, all_affix_rules = affix_setup(WORD_COUNT)', globals=globals())
    difference_update = timeit.Timer(stmt='difference_test_update(wordform_rules, all_affix_rules)', setup='wordform_rules, all_affix_rules = affix_setup(WORD_COUNT)', globals=globals())
    difference_minus = timeit.Timer(stmt='difference_test_minus(wordform_rules, all_affix_rules)', setup='wordform_rules, all_affix_rules = affix_setup(WORD_COUNT)', globals=globals())

    print("Using the difference method, {} repetitions with {} words took {} seconds".format(REPS, WORD_COUNT, difference.timeit(REPS)))
    print("Using the difference update method, {} repetitions with {} words took {} seconds".format(REPS, WORD_COUNT, difference_update.timeit(REPS)))
    print("Using the minus method, {} repetitions with {} words took {} seconds".format(REPS, WORD_COUNT, difference_minus.timeit(REPS)))


def mmap_testing():
    no_mmap = timeit.Timer(stmt='get_affix_rules("/usr/share/myspell/dicts/en_GB-large.aff")', setup='from randword import get_affix_rules')
    with_mmap = timeit.Timer(stmt='get_affix_rules_mmap("/usr/share/myspell/dicts/en_GB-large.aff")', setup='from randword import get_affix_rules_mmap')

    print("Without MMAP, {} repetitions took {} seconds".format(REPS, no_mmap.timeit(REPS)))
    print("With MMAP, {} repetitions took {} seconds".format(REPS, with_mmap.timeit(REPS)))

# Test routines above this line
##################################################
# Helper functions below this line

def affix_setup(word_count):
    dict_name = "en_GB-large"
    dict_path = "/usr/share/myspell/dicts/"
    
    dict_file = dict_path + dict_name + ".dic"
    affix_file = dict_path + dict_name + ".aff"
    
    default_delim = " "
    default_ignore = "M"

    all_affix_rules = randword.get_affix_rules(affix_file)
    wordform_rules = randword.get_words(dict_file, word_count)
    
    return wordform_rules, all_affix_rules
    

def affix_test(wordform_rules, all_affix_rules):
    wordlists = []
    
    for wordform_rule in wordform_rules:
        word_affix_rules = [
                all_affix_rules[affix]
                for affix in tuple(wordform_rule[2])
        ]
        wordlist = randword.apply_affixes(wordform_rule[0], word_affix_rules)
        wordlists.append(wordlist)
    

def affix_test_2(wordform_rules, all_affix_rules):
    wordlists = []
    
    for wordform_rule in wordform_rules:
        word_affix_rules = [
                all_affix_rules[affix]
                for affix in tuple(wordform_rule[2])
        ]
        wordlist = randword.apply_affixes_2(wordform_rule[0], word_affix_rules)
        wordlists.append(wordlist)
        

def difference_test_difference(wordform_rules, all_affix_rules):
    wordlists = []
    all_affixes = set(all_affix_rules.keys())
    affix_ignore_list = set("M")
    
    for wordform_rule in wordform_rules:
        word_affixes = set(wordform_rule[2])
        valid_affixes = word_affixes.intersection(all_affixes)
        usable_affixes = valid_affixes.difference(affix_ignore_list)

        word_affix_rules = [
                all_affix_rules[affix]
                for affix in usable_affixes
        ]


def difference_test_minus(wordform_rules, all_affix_rules):
    wordlists = []
    all_affixes = set(all_affix_rules.keys())
    affix_ignore_list = set("M")
    
    for wordform_rule in wordform_rules:
        word_affixes = set(wordform_rule[2])
        valid_affixes = word_affixes.intersection(all_affixes)
        usable_affixes = valid_affixes - affix_ignore_list

        word_affix_rules = [
                all_affix_rules[affix]
                for affix in usable_affixes
        ]


def difference_test_update(wordform_rules, all_affix_rules):
    wordlists = []
    all_affixes = set(all_affix_rules.keys())
    affix_ignore_list = set("M")
    
    for wordform_rule in wordform_rules:
        word_affixes = set(wordform_rule[2])
        valid_affixes = word_affixes.intersection(all_affixes)
        valid_affixes.difference_update(affix_ignore_list)

        word_affix_rules = [
                all_affix_rules[affix]
                for affix in valid_affixes
        ]


if __name__ == "__main__":
    main()