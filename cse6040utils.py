#!/usr/bin/env python27
"""
Module: cse6040utils

Some utility functions created for Georgia Tech's CSE 6040: Computing for Data Analysis.
"""

import itertools

def keys_geq_threshold (Dict, threshold):
    """
    (Generator) Given a dictionary, yields the keys whose values
    are at or above (greater than or equal to) a given threshold.
    """
    for key, value in Dict.items ():
        if value >= threshold:
            yield key

def alpha_chars (text):
    """
    (Generator) Yields each of the alphabetic characters in a string.
    """
    for letter in text:
        if letter.isalpha ():
            yield letter

def alpha_chars_pairs (text):
    """
    (Generator) Yields every one of the 4-choose-2 pairs of
    'positionally distinct' alphabetic characters in a string.
    
    That is, each position of the string is regarded as distinct,
    but the pair of characters coming from positions (i, j),
    where i != j, are considered the "same" as the paired
    positions (j, i). Non-alphabetic characters should be
    ignored.
    
    For instance, `alpha_chars_pairs ("te3x_t")` should produce
    has just 4 positionally distinct characters, so this routine
    should return the 4 choose 2 == 6 pairs:
      ('t', 'e')    <-- from positions (0, 1)
      ('t', 'x')    <-- from positions (0, 3)
      ('t', 't')    <-- from positions (0, 5)
      ('e', 'x')    <-- from positions (1, 3)
      ('e', 't')    <-- from positions (1, 5)
      ('x', 't')    <-- from positions (3, 5)
    """
    alpha_text = list (alpha_chars (text))
    return itertools.combinations (alpha_text)


from collections import defaultdict

def sparse_vector (base_type=float):
    return defaultdict (base_type)

def print_sparse_vector (x):
    for key, value in x.items ():
        print ("%s: %d" % (key, value))

def sparse_matrix (base_type=float):
    """
    Returns an empty sparse matrix that can hold integer counts
    of pairs of elements.
    """
    return defaultdict (lambda: sparse_vector (base_type))

def print_sparse_matrix (x):
    for i, row_i in x.items ():
        for j, value in row_i.items ():
            print ("[%s, %s]: %d" % (i, j, value))


def dense_vector (n, init_val=0.0):
    """
    [Lab 14] Returns a dense vector of length `n`, with all
    entries set to `init_val`.
    """
    return [init_val] * n

def spmv (n, A, x):
    """
    [Lab 14] Returns a dense vector y of length n, where
    y = A*x.
    """
    y = dense_vector (n)
    for (i, A_i) in A.items ():
        s = 0
        for (j, a_ij) in A_i.items ():
            s += a_ij * x[j]
        y[i] = s
    return y

import math

def vec_scale (x, alpha):
    """[Lab 14] Scales the vector x by a constant alpha."""
    return [x_i*alpha for x_i in x]

def vec_add_scalar (x, c):
    """[Lab 14] Adds the scalar value c to every element of x."""
    return [x_i+c for x_i in x]

def vec_sub (x, y):
    """[Lab 14] Returns x - y"""
    return [x_i - y_i for (x_i, y_i) in zip (x, y)]

def vec_2norm (x):
    """[Lab 14] Returns ||x||_2"""
    return math.sqrt (sum ([x_i**2 for x_i in x]))


import pandas as pd
import sys

def pandas2sqlite (df_reader, sql_writer, table_name, capitalize=False):
    """
    Given a text file reader for a Pandas data frame, creates an SQLite
    table. Returns the number of rows read.
    """
    index_start = 0
    for df in df_reader:
	if capitalize:
	    df.columns = [x.capitalize () for x in df.columns.values]
        action = 'replace' if (index_start == 1) else 'append'
        df.to_sql (table_name, sql_writer, if_exists=action)
        index_start += len (df)
        
        print ("(Processed %d records.)" % index_start)
        sys.stdout.flush ()
    return index_start

def peek_table (db, name):
    """
    [Lab 14] Given a database connection (`db`), prints both the number of
    records in the table as well as its first few entries.
    """
    count = '''SELECT COUNT (*) FROM {table}'''.format (table=name)
    display (pandas.read_sql_query (count, db))
    peek = '''SELECT * FROM {table} LIMIT 5'''.format (table=name)
    display (pandas.read_sql_query (peek, db))


# [Lab 21] Floating-point utilities
# See also: https://docs.python.org/2/tutorial/floatingpoint.html
import re

RE_FLOAT_HEX_PARTS = re.compile (r'''^(?P<sign>-)?0x1\.(?P<mantissa>[0-9a-f]+)p(?P<signexp>[+-])(?P<exp>\d+)''')

def float_to_bin (x):
    """Given a `float`, returns its binary form as a string."""
    assert type (x) is float
    s_hex = float.hex (x)
    hex_parts = RE_FLOAT_HEX_PARTS.match (s_hex)
    assert hex_parts
    
    s = hex_parts.group ('sign')
    m = hex_parts.group ('mantissa')
    se = hex_parts.group ('signexp')
    e = hex_parts.group ('exp')
    
    # Mantissa, including sign bit
    # See also: http://stackoverflow.com/questions/1425493/convert-hex-to-binary
    s_bin = '['
    if s:
        s_bin += s
    s_bin += \
        "1." \
        + bin (int (m, 16))[2:].zfill (4 * len (m)) \
        + "]_{2}"
    
    # Sign of exponent
    s_bin += "e" + se
    
    # Exponent
    s_bin += e

    return s_bin


if __name__ == "__main__":
    print __doc__

# eof
