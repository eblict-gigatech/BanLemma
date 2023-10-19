"""
This module holds the Parts of Speech (PoS) related functionalities.
"""

import os
import sys
from collections import defaultdict
from typing import List, Tuple

import bnlp

try:
    from bnlp import POS as bnlp_pos
except:
    from bnlp import BengaliPOS as bnlp_pos


try:
    package_path = os.path.dirname(sys.modules["banlemma"].__file__)
except:
    package_path = "banlemma"

model_path = os.path.join(package_path, "data", "bnlp_models", "bn_pos.pkl")

if bnlp.__version__ < "4.0.0":
    pos = bnlp_pos()
else:
    pos = bnlp_pos(model_path=model_path)

pos_map = defaultdict(lambda: "words")
pos_map["N"] = "nouns"
pos_map["R"] = "adverbs"
pos_map["V"] = "verbs"
pos_map["J"] = "adjectives"


def get_pos_tags(text: str) -> List[Tuple[str, str]]:
    """Return the words and pos tags of a text.

    Args:
        text (str): The text to get PoS tags.

    Returns:
        List[Tuple[str, str]]: A list of (word, pos) tuples.
    """
    if bnlp.__version__ < "4.0.0":
        tags = pos.tag(model_path, text)
    else:
        tags = pos.tag(text)

    return tags
