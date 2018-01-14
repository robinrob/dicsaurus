# Dicsaurus
Dicsaurus uses the Oxford English Dictionary API to implement command-line dicsaurus and thesaurus functionality.

## Setup
1. Register for an Oxford Dictionaries [developer account](https://developer.oxforddictionaries.com/).
2. Create a new `config.py` from `config_example.py` and enter your `app_id` and `app_key` into `config.py`.
3. Run dicsaurus: `./dicsaurus.py --help`.

## Examples

### Dictionary:
`./dicsaurus.py bird`

### Thesaurus:
`./dicsaurus.py -t bird`

## Customization
Just modify the `print_*` functions in `dicsaurus.py`.