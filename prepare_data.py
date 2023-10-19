"""
Read all text (.txt) files from a directory and prepare the markers dictionary.
The markers are needed to lemmatize nouns, pronouns, adjectives, adverbs and 
post postposition. To lemmatize verb, suffixes must be prepared using the 
'data_preparation/utils/prepare_suffixes_dict.py' script.
"""

import os
import json
import pickle
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Dictionary, markers and suffixes preparation for the lemmatizer"
    )

    parser.add_argument(
        "--dictionary", type=str, help="File path to the word-lemma dictionary."
    )
    parser.add_argument(
        "--markers_dir",
        type=str,
        help="Directory path containing list of markers' files.",
    )
    parser.add_argument(
        "--verb_suffixes", type=str, help="File path to the list of verb suffixes"
    )
    parser.add_argument(
        "--save_dir", type=str, default="banlemma/data", help="Save directory path."
    )

    args = parser.parse_args()
    os.makedirs(args.save_dir, exist_ok=True)

    assert args.dictionary.endswith("json"), "Dictionary muse be a JSON file."

    if args.dictionary is not None:
        dictionary_file = open(args.dictionary)
        dictionary = json.load(dictionary_file)

        save_file_path = os.path.join(args.save_dir, "dictionary.pkl")
        with open(save_file_path, "wb") as save_file:
            pickle.dump(dictionary, save_file)

        print(f"Prepared dictionary and saved in {save_file_path}")

    if args.markers_dir is not None:
        all_markers = {}
        for file_name in os.listdir(args.markers_dir):
            marker_type = file_name.split(".")[0]
            file_path = os.path.join(args.markers_dir, file_name)

            markers = set()
            with open(file_path) as f:
                for line in f:
                    line = line.strip()

                    if line:
                        markers.add(line)

            markers = sorted(markers, key=lambda x: len(x), reverse=True)
            all_markers[marker_type] = markers

        save_file_path = os.path.join(args.save_dir, "markers.pkl")
        with open(save_file_path, "wb") as save_file:
            pickle.dump(all_markers, save_file)

        print(f"Prepared markers and saved in {save_file_path}")

    if args.verb_suffixes is not None:
        suffixes = set()
        with open(args.verb_suffixes) as f:
            for line in f:
                line = line.strip()

                if line:
                    suffixes.add(line)
        suffixes = sorted(suffixes, key=lambda x: len(x), reverse=True)
        suffixes = {"verbs": suffixes}

        save_file_path = os.path.join(args.save_dir, "suffixes.pkl")
        with open(save_file_path, "wb") as save_file:
            pickle.dump(suffixes, save_file)

        print(f"Prepared verb suffixes and saved in {save_file_path}")
