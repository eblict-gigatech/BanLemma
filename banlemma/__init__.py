"""
This module contains functionalities to lemmatize Bangla text. The lemmatization can
be done at both sentence level and word level.
"""

from . import utils
from ._lemmatize import lemmatize, lemmatize_word

__all__ = ["lemmatize", "lemmatize_word", "utils"]
