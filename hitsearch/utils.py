"""
    utils.py

    Contains a function to make strings into a consistent ASCII form without
    punctuation.
"""

import string, unicodedata

def sanitize(s):
    """Normalizes a unicode string to ASCII by removing accents and ignoring
       all other non-ASCII characters. Then removes punctuation."""
    # inspired by http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
    # and http://snippets.dzone.com/posts/show/5499

    normalized = unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')
    out = normalized.translate(string.maketrans("",""), string.punctuation)
    return out
