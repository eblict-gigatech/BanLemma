import argparse

from banlemma import utils


def lemmatize(text: str, with_pos: bool = False) -> str:
    """Lemmatize given text (sentence level) and return the lemmatized text.

    Args:
        text (str): The text to lemmatize.
        debug (bool, optional): Whether to return debug information. Defaults to False.
        with_pos (bool, optional): Whether to return predicted PoS tags. Defaults to False.

    Returns:
        str: The lemmatized text.

    Examples:
        >>> import bkit
        >>> text = 'পৃথিবীর জনসংখ্যা ৮ বিলিয়নের কিছু কম'
        >>> bkit.lemmatizer.lemmatize(text)
        'পৃথিবী জনসংখ্যা ৮ বিলিয়ন কিছু কম'
        >>>
        >>> bkit.lemmatizer.lemmatize(text, debug=True)
        '(n2 পৃথিবী) (n2 জনসংখ্যা) (adv ৮) (n2 বিলিয়ন) (adj কিছু) (adj কম)'
        >>>
        >>> bkit.lemmatizer.lemmatize(text, with_pos=True)
        'পৃথিবী/NN জনসংখ্যা/NN ৮/ADV বিলিয়ন/NN কিছু/ADJ কম/ADJ'
    """
    pos_tags = utils.pos.get_pos_tags(text)

    lemmas = []
    for word, tag in pos_tags:
        if tag == "PPR":
            lemma = utils.lemmatize.lemmatize_pronoun(word)

            if with_pos:
                lemmas.append(f"{lemma}/PRO")
            else:
                lemmas.append(lemma)
        elif tag == "PP":
            lemma = utils.lemmatize.lemmatize_postposition(word)

            if with_pos:
                lemmas.append(f"{lemma}/PP")
            else:
                lemmas.append(lemma)
        elif utils.pos.pos_map[tag[0]] == "nouns":
            lemma = utils.lemmatize.lemmatize_noun(word)

            if with_pos:
                lemmas.append(f"{lemma}/NN")
            else:
                lemmas.append(lemma)
        elif utils.pos.pos_map[tag[0]] == "verbs":
            lemma = utils.lemmatize.lemmatize_verb(word)

            if with_pos:
                lemmas.append(f"{lemma}/VRB")
            else:
                lemmas.append(lemma)
        elif utils.pos.pos_map[tag[0]] == "adverbs":
            lemma = utils.lemmatize.lemmatize_adverb(word)

            if with_pos:
                lemmas.append(f"{lemma}/ADV")
            else:
                lemmas.append(lemma)
        elif utils.pos.pos_map[tag[0]] == "adjectives":
            lemma = utils.lemmatize.lemmatize_adjective(word)

            if with_pos:
                lemmas.append(f"{lemma}/ADJ")
            else:
                lemmas.append(lemma)
        else:
            if with_pos:
                lemmas.append(f"{word}/O")
            else:
                lemmas.append(word)

    return " ".join(lemmas)


def lemmatize_word(word: str, pos: str) -> str:
    """Lemmatize a word based on the given Parts of Speech (PoS) tag.

    Args:
        word (str): The word to lemmatize.
        pos (str): PoS tag of the given word. The tag must be one of *['noun',
            'pronoun', 'adjective', 'verb', 'adverb', 'conjunction', 'interjection',
            'postposition', 'others', 'part', 'punctuation']*.

    Returns:
        str: The lemmatized word.

    Examples:
        >>> import bkit
        >>> bkit.lemmatizer.lemmatize_word('পৃথিবীর', 'noun')
        'পৃথিবী'
    """
    allowed_pos = [
        "noun",
        "pronoun",
        "adjective",
        "verb",
        "adverb",
        "conjunction",
        "interjection",
        "postposition",
        "others",
        "part",
        "punctuation",
    ]
    assert (
        pos in allowed_pos
    ), f"Provided POS `{pos}` is not allowed. Must be one of {allowed_pos}"

    assert len(word.split()) == 1, (
        "There must be one word only. If you are looking to lemmatize "
        "multi-word text, use the `lemmatize` method."
    )

    if pos == "pronoun":
        lemma = utils.lemmatize.lemmatize_pronoun(word)
    elif pos == "postposition":
        lemma = utils.lemmatize.lemmatize_postposition(word)
    elif pos == "noun":
        lemma = utils.lemmatize.lemmatize_noun(word)
    elif pos == "verb":
        lemma = utils.lemmatize.lemmatize_verb(word)
    elif pos == "adverb":
        lemma = utils.lemmatize.lemmatize_adverb(word)
    elif pos == "adjective":
        lemma = utils.lemmatize.lemmatize_adjective(word)
    else:
        lemma = word

    return lemma


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Bangla lemmatizer")
    parser.add_argument("text", help="Text to lemmatize")
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    lemmas = lemmatize(args.text, args.debug)
    print(lemmas)
