"""
This module holds the lemmatization functions of each PoS type.
"""

import os
import pickle
import sys

try:
    package_path = os.path.dirname(sys.modules["banlemma"].__file__)
except:
    package_path = "banlemma"

path = os.path.join(package_path, "data", "dictionary.pkl")
vocab_file = open(path, "rb")
vocab = pickle.load(vocab_file)

path = os.path.join(package_path, "data", "suffixes.pkl")
rules_file = open(path, "rb")
rules = pickle.load(rules_file)

path = os.path.join(package_path, "data", "markers.pkl")
suffixes_file = open(path, "rb")
suffixes = pickle.load(suffixes_file)


def lemmatize_noun(word: str) -> str:
    """Lemmatize a noun word utilizing a list of markers and word formation rules.

    Args:
        word (str): The word to lemmatize.

    Returns:
        str: The lemmatized word.
    """
    word = word.strip()

    if word in vocab["nouns"]:
        return vocab["nouns"][word]

    # remove emphasis
    max_suffix_len, max_suffix = -1, ""
    for suffix in suffixes["emphasis"]:
        if word.endswith(suffix):
            temp_word = word[: -len(suffix)]
            if temp_word in vocab["nouns"]:
                return vocab["nouns"][temp_word]

            elif len(suffix) > max_suffix_len:
                max_suffix = suffix
                max_suffix_len = len(suffix)

    if max_suffix_len > 0:
        word = word[: -len(max_suffix)]

    # remove case marker
    max_suffix_len, max_suffix = -1, ""
    for suffix in suffixes["cases"]:
        if word.endswith(suffix):
            temp_word = word[: -len(suffix)]
            if temp_word and temp_word[-1] == "্":
                continue

            if temp_word in vocab["nouns"]:
                return vocab["nouns"][temp_word]

            elif len(suffix) > max_suffix_len:
                max_suffix = suffix
                max_suffix_len = len(suffix)

    if max_suffix_len > 0:
        if max_suffix == "ের" and word.endswith("দের"):
            max_suffix = "দের"

        if max_suffix == "র":
            if word.endswith("দের"):
                max_suffix = "দের"
            elif word.endswith("্র"):
                max_suffix = ""
            elif word.endswith("নগর"):
                max_suffix = ""

        word = word[: -len(max_suffix)]
        if word in vocab["nouns"]:
            return vocab["nouns"][word]

    # remove determiner
    determiner_matched = False
    max_suffix_len, max_suffix = -1, ""
    for suffix in suffixes["determiners"]:
        if word.endswith(suffix):
            determiner_matched = True
            temp_word = word[: -len(suffix)]
            if temp_word and temp_word[-1] == "্":
                continue

            if temp_word in vocab["nouns"]:
                return vocab["nouns"][temp_word]

            elif len(suffix) > max_suffix_len:
                max_suffix = suffix
                max_suffix_len = len(suffix)

    if max_suffix_len > 0:
        word = word[: -len(max_suffix)]

    # Check case again only if got a determiner match as
    # we already checked case once. So, we need to check
    # case again only if we got a determiner match
    if determiner_matched:
        max_suffix_len, max_suffix = -1, ""
        for suffix in suffixes["cases"]:
            if word.endswith(suffix):
                temp_word = word[: -len(suffix)]
                if temp_word and temp_word[-1] == "্":
                    continue

                if temp_word in vocab["nouns"]:
                    return vocab["nouns"][temp_word]

                elif len(suffix) > max_suffix_len:
                    max_suffix = suffix
                    max_suffix_len = len(suffix)

        if max_suffix_len > 0:
            word = word[: -len(max_suffix)]

    # check plural marker
    plural_matched = False
    max_suffix_len, max_suffix = -1, ""
    for suffix in suffixes["plurals"]:
        if word.endswith(suffix):
            plural_matched = True
            temp_word = word[: -len(suffix)]
            if temp_word and temp_word[-1] == "্":
                continue

            if temp_word in vocab["nouns"]:
                return vocab["nouns"][temp_word]

            elif len(suffix) > max_suffix_len:
                max_suffix = suffix
                max_suffix_len = len(suffix)

    if max_suffix_len > 0:
        word = word[: -len(max_suffix)]

    # if got a plural match previous step, check if there is a case
    # marker match again.
    if plural_matched:
        max_suffix_len, max_suffix = -1, ""
        for suffix in suffixes["cases"]:
            if word.endswith(suffix):
                temp_word = word[: -len(suffix)]
                if temp_word and temp_word[-1] == "্":
                    continue

                if len(suffix) > max_suffix_len:
                    max_suffix = suffix
                    max_suffix_len = len(suffix)

        if max_suffix_len > 0:
            word = word[: -len(max_suffix)]

    return word


def lemmatize_pronoun(word: str) -> str:
    """Lemmatize a pronoun utilizing a list of markers and word formation rules.

    Args:
        word (str): The word to lemmatize.

    Returns:
        str: The lemmatized word.
    """
    word = word.strip()

    if word in vocab["pronouns"]:
        return vocab["pronouns"][word]

    # remove emphasis
    max_suffix_len, max_suffix = -1, ""
    for suffix in suffixes["emphasis"]:
        if word.endswith(suffix):
            temp_word = word[: -len(suffix)]
            if temp_word in vocab["pronouns"]:
                return vocab["pronouns"][temp_word]

            elif len(suffix) > max_suffix_len:
                max_suffix = suffix
                max_suffix_len = len(suffix)

    if max_suffix_len > 0:
        word = word[: -len(max_suffix)]

    # remove case marker
    max_suffix_len, max_suffix = -1, ""
    for suffix in suffixes["cases"]:
        if word.endswith(suffix):
            temp_word = word[: -len(suffix)]
            if temp_word in vocab["pronouns"]:
                return vocab["pronouns"][temp_word]

            elif len(suffix) > max_suffix_len:
                max_suffix = suffix
                max_suffix_len = len(suffix)

    if max_suffix_len > 0:
        if max_suffix == "ের" and word.endswith("দের"):
            max_suffix = "দের"

        word = word[: -len(max_suffix)]

    # remove determiner
    determiner_matched = False
    max_suffix_len, max_suffix = -1, ""
    for suffix in suffixes["determiners"]:
        if word.endswith(suffix):
            determiner_matched = True
            temp_word = word[: -len(suffix)]
            if temp_word in vocab["pronouns"]:
                return vocab["pronouns"][temp_word]

            elif len(suffix) > max_suffix_len:
                max_suffix = suffix
                max_suffix_len = len(suffix)

    if max_suffix_len > 0:
        word = word[: -len(max_suffix)]

    # Check case again only if got a determiner match as
    # we already checked case once. So, we need to check
    # case again only if we got a determiner match
    if determiner_matched:
        max_suffix_len, max_suffix = -1, ""
        for suffix in suffixes["cases"]:
            if word.endswith(suffix):
                temp_word = word[: -len(suffix)]
                if temp_word in vocab["pronouns"]:
                    return vocab["pronouns"][temp_word]

                elif len(suffix) > max_suffix_len:
                    max_suffix = suffix
                    max_suffix_len = len(suffix)

        if max_suffix_len > 0:
            word = word[: -len(max_suffix)]

    return word


def lemmatize_adjective(word: str):
    """Lemmatize an adjective utilizing a list of markers and word formation rules.

    Args:
        word (str): The word to lemmatize.

    Returns:
        str: The lemmatized word.
    """
    word = word.strip()

    if word in vocab["adjectives"]:
        return vocab["adjectives"][word]

    for suffix in suffixes["emphasis"]:
        if word.endswith(suffix):
            word = word[: -len(suffix)]
            if word in vocab["adjectives"]:
                return vocab["adjectives"][word]
            break

    for suffix in suffixes["degree"]:
        if word.endswith(suffix):
            word = word[: -len(suffix)]
            break

    return word


def lemmatize_verb(word: str):
    """Lemmatize a verb utilizing a list of suffixes.

    Args:
        word (str): The word to lemmatize.

    Returns:
        str: The lemmatized word.
    """
    word = word.strip()

    if word in vocab["verbs"]:
        return vocab["verbs"][word]

    for emphasis in ["ই", "ও", "ঃ"]:
        if word.endswith(emphasis):
            word = word[:-1]

    max_suffix_len, max_suffix = -1, ""
    for suffix in rules["verbs"]:
        if word.endswith(suffix):
            lemma = word[: -len(suffix)]
            if lemma and lemma[-1] == "্":
                continue

            if lemma in vocab["verbs"]:
                return vocab["verbs"][lemma]
            elif len(suffix) > max_suffix_len:
                max_suffix = suffix
                max_suffix_len = len(suffix)

    if max_suffix_len > 0:
        return word[: -len(max_suffix)]
    else:
        return word


def lemmatize_adverb(word: str) -> str:
    """Lemmatize an adverb utilizing a list of markers and word formation rules.

    Args:
        word (str): The word to lemmatize.

    Returns:
        str: The lemmatized word.
    """
    word = word.strip()

    if word in vocab["adverbs"]:
        return vocab["adverbs"][word]

    # remove emphasis
    for suffix in suffixes["emphasis"]:
        if word.endswith(suffix):
            word = word[: -len(suffix)]
            if word in vocab["adverbs"]:
                return vocab["adverbs"][word]
            break

    return word


def lemmatize_postposition(word: str) -> str:
    """Lemmatize a post-position utilizing a list of markers and word formation rules.

    Args:
        word (str): The word to lemmatize.

    Returns:
        str: The lemmatized word.
    """
    word = word.strip()

    if word in vocab["postpositions"]:
        return vocab["postpositions"][word]

    # remove emphasis
    for suffix in suffixes["emphasis"]:
        if word.endswith(suffix):
            word = word[: -len(suffix)]
            if word in vocab["postpositions"]:
                return vocab["postpositions"][word]
            break

    return word
