#!/usr/bin/env python

from __future__ import print_function

info = r'''Find anagrams of letters

Dictionary options are:
    SSWL15 - School Scrabble 2015
    TWL06  - Tournament word list 2006
    OWL14  - Tournament word list 2014
    CSW12  - Collins word list 2012
    OSPD4  - Official Scrabble Players Dictionary 4th edition
'''

freq = 'QJXZWKVFYBHGMPUDCLOTNRAISE' # Frequency order obtained from counting word.lst
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
prime_dict = {freq[i]:primes[i] for i in range(26)} # Match common letters with small primes

def freq_sort(letters):
    '''Sort letters according to frequency.
    >>> freq_sort('QUINZHEE')
    ['Q', 'Z', 'H', 'U', 'N', 'I', 'E', 'E']
    '''
    return sorted(letters, key=lambda c: freq.find(c))

def least_common_letter_included(letters):
    '''Filter on the least common letter in letters.
    str -> str -> Bool
    >>> least_common_letter_included('QADI')('QJX')
    True
    '''
    for ch in freq:
        if ch in letters:
            break
    else:
        raise TypeError
    return lambda word: ch in word

def least_common_letter(letters):
    '''Find the least common letter in letters.
    str -> str
    >>> least_common_letter('QADI')
    'Q'
    '''
    for ch in freq:
        if ch in letters:
            return ch
    else:
        raise TypeError

def most_common_letter_excluded(letters):
    '''Filter on the least common letter in letters.
    str -> str -> Bool
    >>> most_common_letter_excluded('QADI')('QJX')
    True
    '''
    freq = 'QJXZWKVFYBHGMPUDCLOTNRAISE' # Frequency order obtained from counting word.lst
    for ch in freq[::-1]:
        if ch not in letters:
            break
    else:
        raise TypeError
    return lambda word: ch not in word

def most_common_letter_missing(letters):
    '''Return the most common letter missing from <letters>.
    >>> most_common_letter_missing('QADI')
    'E'
    '''
    for ch in freq[::-1]:
        if ch not in letters:
            return ch
    else:
        raise TypeError

def prime_value(letters):
    result = 1
    for ch in letters:
        result *= prime_dict[ch]
    return result

def contains_filter(letters, stream):
    '''Filters out words in stream that contain all the letters.
    More general than anagram filter. Useful for anagrams with blanks.
    '''
    def product(L):
        result = 1
        for i in L:
            result *= i
        return result
    p = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
    freq = 'QJXZWKVFYBHGMPUDCLOTNRAISE' # Frequency order obtained from counting word.lst
    D = {freq[i]:p[i] for i in range(26)} # Match common letters with small primes
    n = product((D[ch] for ch in letters))
    for line in stream:
        if product((D[ch] for ch in line[:-1]))%n == 0:
            yield line

def prepQuery(query):
    '''Prepare incoming query for stream testing.
    Uppercase all letters. Replace all "blanks" with the "@" symbol.
    '''
    query = query.upper()
    query = query.replace('_', '@')
    query = query.replace('?', '@')
    blanks = query.count('@')
    letters = sorted(query.replace('@', ''))
    return letters, blanks

def len_range(start, stop):
    '''Returns a function that recognizes words with length in [start, stop).
    (int, int) -> str -> Bool
    >>> len_range(4,5)('HELP')
    True
    '''
    # If words are not ordered in increasing word length, use the following.
    # return lambda word: len(word) < stop and len(word) >= start
    def len_filter(word):
        n = len(word)
        if n < start:
            return False
        if n >= stop:
            raise StopIteration
        return True
    return len_filter

DICT = ['SSWL15', 'TWL06', 'OWL14', 'CSW12', 'OSPD4']

def all_func(F):
    '''Return a function that is the logical and of input functions.
    Equivalent, but faster than lambda x: all(f(x) for f in F
    F must be repeatably iterable.
    '''
    F = tuple(F)
    def multi_filter(x):
        for f in F:
            if not f(x):
                return False
        return True
    return multi_filter

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description=info,
                formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d', '--dict', action='store', dest='dict',
                default='OWL14', help='Choose dictionary.')
    parser.add_argument('--min', type=int, action='store', dest='min', default=None)
    parser.add_argument('--max', type=int, action='store', dest='max', default=None)
    parser.add_argument('-a', '--all', action='store_true', dest='all', 
                default=False, help='Return all anagrams of length 3 or more.')
    parser.add_argument('letters', nargs='?', type=str, help='Letters to anagram.')
    results = parser.parse_args()

    # Abort if dictionary is not valid
    if results.dict not in DICT:
        print('Error: Invalid dictionary', file=sys.stderr)
        exit(-1)

    # Abort if no letters were provided
    if results.letters is None:
        parser.print_help()
        exit(-1)

    letters, blanks = prepQuery(results.letters)
    L = {letter:letters.count(letter) for letter in letters}
    if results.min is None:
        results.min = len(letters) + blanks
    if results.max is None:
        results.max = len(letters) + blanks
    if results.max < results.min:
        parser.print_help()
        exit(-1)
    if results.all:
        results.min = 3
    txt_file = '/usr/share/dict/'+results.dict+'.txt'
    with open(txt_file, 'rt') as infile:
        words = (line.strip() for line in infile)
        for word in words:
            if len(word) < results.min:
                continue
            if len(word) > results.max:
                continue
            target = len(word)
            for letter in L:
                target -= min(L[letter], word.count(letter))
            if target <= blanks:
                print(word)
