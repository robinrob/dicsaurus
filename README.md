# Dictionary
Dictionary uses the Oxford English Dictionary API to implement dictionary and thesaurus functionality.

## Setup
1. Register for an Oxford Dictionaries [developer account](https://developer.oxforddictionaries.com/).
2. Enter your `app_id` and `app_key` into `config.json`
3. Run dictionary: `./dictionary.py --help`

## Examples
Dictionary:
`./dictionary.py bird`

Thesaurus
`./dictionary.py -t bird

## Customization
Just modify the `print_*` functions in `dictionary.py`.