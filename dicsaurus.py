#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse
import argparse
import config


BASE_URL = 'https://od-api.oxforddictionaries.com/api/v1'

INDENT_UNIT = "   "


def print_with_indent(str, indent=0, with_preceding_newlines=0):
    if with_preceding_newlines > 0:
        print('\n' * (with_preceding_newlines-1))

    print(f"{INDENT_UNIT * indent}{str}")


def get_definitions(config, word):
    req = urllib.request.Request(
        "{base_url}/entries/en/{word}".format(
            base_url=BASE_URL,
            word=word
        ),
        headers={
            'app_id': config.APP_ID,
            'app_key': config.APP_KEY
        }
    )
    res = urllib.request.urlopen(req).read()
    return json.loads(res)


def print_definitions(word, data):
    print_with_indent(f"Definition(s) for '{word}'", with_preceding_newlines=1)
    for result in data['results']:
        for index, lex_entry in enumerate(result['lexicalEntries']):
            print_with_indent(
                f"{lex_entry['text']} ({lex_entry['lexicalCategory']})",
                1,
                with_preceding_newlines=1 if index == 0 else 2
            )

            examples = []
            etymologies = []

            if 'derivative' in lex_entry and len(lex_entry['derivatives']) > 0:
                print_with_indent(f"Derivative(s):", 2, with_preceding_newlines=1)

                for derivative in lex_entry['derivatives']:
                    print_with_indent(f"{derivative['text']}", 3)

            for entry in lex_entry['entries']:
                if len(entry['senses']) > 0:
                    for sense in entry['senses']:
                        if 'examples' in sense:
                            for example in sense['examples']:
                                examples.append(example)

                if 'etymologies' in entry:
                    for et in entry['etymologies']:
                        etymologies.append(et)

            if len(examples) > 0:
                print_with_indent(f"Example(s):", 2, with_preceding_newlines=1)

                for example in examples:
                    print_with_indent(f"{example['text']}", 3)


            if len(etymologies) > 0:
                print_with_indent(f"Etomologie(s):", 2, with_preceding_newlines=1)

                for et in etymologies:
                    print_with_indent(f"{et}", 3)


def get_synonyms(config, word):
    req = urllib.request.Request(
        "{base_url}/entries/en/{word}/synonyms".format(
            base_url=BASE_URL,
            word=word
        ),
        headers={
            'app_id': config.APP_ID,
            'app_key': config.APP_KEY
        }
    )
    res = urllib.request.urlopen(req).read()
    return json.loads(res)


def print_synonyms(word, data):
    print_with_indent(f"Synonym(s) for '{word}'", with_preceding_newlines=1)

    for result in data['results']:
        for lex_entry in result['lexicalEntries']:
            print_with_indent(f"{lex_entry['text']} ({lex_entry['lexicalCategory']})", 1, with_preceding_newlines=1)

            for entry in lex_entry['entries']:
                for sense in entry['senses']:
                    synonyms = []
                    examples = []

                    # if 'registers' in sense:
                    #     registers = ", ".join(sense['registers'])
                    #     print_with_indent(f"{lex_entry['text']} ({registers})", 1, with_preceding_newlines=2)

                    if len(sense['synonyms']) > 0:
                        for syn in sense['synonyms']:
                            synonyms.append(syn)

                    if 'examples' in sense:
                        for example in sense['examples']:
                            examples.append(example)


                    if len(synonyms) > 0:
                        print_with_indent("Snynoym(s):", 2, with_preceding_newlines=1)

                        for syn in synonyms:
                            print_with_indent(f"{syn['text']}", 3)


                    if len(examples) > 0:
                        print_with_indent(f"Example(s):", 2, with_preceding_newlines=1)

                        for example in examples:
                            print_with_indent(f"{example['text']}", 3)

                    # if 'subsenses' in sense:
                    #     print_with_indent(f"Example(s):", 2, with_preceding_newlines=1)
                    #
                    #     for subsense in sense['subsenses']:
                    #         for syn in subsense['synonyms']:
                    #             print_with_indent(f"{syn['text']}", 3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get dictionary/thesaurus entries for words.')

    parser.add_argument(
        'word',
        metavar='word',
        help='Word to search for'
    )

    parser.add_argument(
        '-t',
        action='store_const',
        const=True,
        dest='thesaurus_mode',
        help='Use dictionary in thesaurus mode'
    )

    args = parser.parse_args()
    word = args.word

    try:
        if args.thesaurus_mode:
            data = get_synonyms(config, word)
        else:
            data = get_definitions(config, args.word)

        if len(data['results']) > 0:
            print(f"Results from {data['metadata']['provider']}:")

        if args.thesaurus_mode:
            print_synonyms(word, data)
        else:
            print_definitions(word, data)

    except urllib.error.HTTPError as e:
        if 'NOT FOUND' in e.msg:
            print("No results")
        else:
            print(f"ERROR: {e.msg}")


