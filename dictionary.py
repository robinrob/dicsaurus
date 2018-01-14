#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse
import argparse


BASE_URL = 'https://od-api.oxforddictionaries.com/api/v1'


def get_indent(nesting=1):
    return "   " * nesting


def get_definitions(config, word):
    req = urllib.request.Request(
        "{base_url}/entries/en/{word}".format(
            base_url=BASE_URL,
            word=args.word
        ),
        headers={
            'app_id': config['app_id'],
            'app_key': config['app_key']
        }
    )
    res = urllib.request.urlopen(req).read()
    return json.loads(res)


def print_definitions(word, data):
    for result in data['results']:
        print("\nDefinitions:")

        for lex_entry in result['lexicalEntries']:
            indent = get_indent()

            print(f"\n{indent}{lex_entry['text']} ({lex_entry['lexicalCategory']})")

            if 'derivatives' in lex_entry and len(lex_entry['derivatives']) > 0:
                print(f"\n{indent}Derivatives:")
                indent = get_indent(2)
                for derivative in lex_entry['derivatives']:
                    # print('derivative: %s' % derivative)
                    print(f"{indent}{derivative['text']}")

            for entry in lex_entry['entries']:
                if len(entry['senses']) > 0:
                    indent = get_indent(1)
                    print(f"\n{indent}Senses:")
                    indent = get_indent(2)
                    for sense in entry['senses']:
                        if 'examples' in sense:
                            for example in sense['examples']:
                                print(f"{indent}{example['text']}")

                if 'etymologies' in entry:
                    indent = get_indent(1)
                    print(f"\n{indent}Etomologies:")

                    indent = get_indent(2)
                    for et in entry['etymologies']:
                        print(f"{indent}{et}:")


def get_synonyms(config, word):
    req = urllib.request.Request(
        "{base_url}/entries/en/{word}/synonyms".format(
            base_url=BASE_URL,
            word=args.word
        ),
        headers={
            'app_id': config['app_id'],
            'app_key': config['app_key']
        }
    )
    res = urllib.request.urlopen(req).read()
    return json.loads(res)


def print_synonyms(word, data):
    for result in data['results']:
        for lex_entry in result['lexicalEntries']:
            for entry in lex_entry['entries']:
                for sense in entry['senses']:
                    print("\nSnynoyms:")

                    if len(sense['synonyms']) > 0:
                        indent = get_indent()
                        for syn in sense['synonyms']:
                            print(f"{indent}{syn['text']}")

                        if 'subsenses' in sense:
                            subsenses = sense['subsenses']
                            print(f"\n{indent}Sub-senses:")
                            indent = get_indent(2)
                            try:
                                # For god's sake this subscript works but raises a KeyError ...
                                for subsense in subsenses:
                                    for syn in subsense['synonyms']:
                                        print(f"{indent} {syn['text']}")

                            except KeyError:
                                pass


if __name__ == '__main__':
    config = json.loads(open('config.json').read())

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


