# Other Solution for Stage 1

```python
MAIN_MENU = {
    'name': 'MAIN MENU',
    '0': 'Exit',
    '1': 'CRUD operations',
    '2': 'Show top ten companies by criteria',
}

CRUD_MENU = {
    'name': 'CRUD MENU',
    '0': 'Back',
    '1': 'Create a company',
    '2': 'Read a company',
    '3': 'Update a company',
    '4': 'Delete a company',
    '5': 'List all companies',
}

TOP_TEN_MENU = {
    'name': 'TOP TEN MENU',
    '0': 'Back',
    '1': 'List by ND/EBITDA',
    '2': 'List by ROE',
    '3': 'List by ROA',
}


def main() -> None:
    match get_option(MAIN_MENU):
        case '0':
            print('Have a nice day!')
        case '1':
            crud()
        case '2':
            top_ten()


def crud() -> None:
    match get_option(CRUD_MENU):
        case '0':
            main()
        case _:
            print('Not implemented!')
            main()


def top_ten() -> None:
    match get_option(TOP_TEN_MENU):
        case '0':
            main()
        case _:
            print('Not implemented!')
            main()


def get_option(menu: dict[str, str]) -> str:
    while (option := input(get_menu(menu))) not in menu:
        print('Invalid option!')
    return option


def get_menu(menu: dict[str, str]) -> str:
    menu_string = '\n'.join(f'{k} {v}' for k, v in menu.items() if k != 'name')
    return f'\n{menu["name"]}\n{menu_string}\n\nEnter an option:\n'


if __name__ == '__main__':
    main()
```