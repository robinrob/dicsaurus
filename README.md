# Dicsaurus
Dicsaurus uses the Oxford English Dictionary API to implement command-line dicsaurus and thesaurus functionality.

## Setup
1. Install Python 3 if not already installed
2. In project folder, create a Python 3 virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `. ./venv/bin/activate`
4. Register for an Oxford Dictionaries [developer account](https://developer.oxforddictionaries.com/).
5. Create a new `config.py` from `config_example.py` and enter your `app_id` and `app_key` into `config.py`.
6. Run dicsaurus: `./dicsaurus.py --help`.

## Examples

### Dictionary:
`./dicsaurus.py bird`

### Thesaurus:
`./dicsaurus.py -t bird`

## Customization
Just modify the `print_*` functions in `dicsaurus.py`.
