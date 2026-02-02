COMMANDS_MAIN = {"0": "0",
                 "1": "1",
                 "2": "2"}

COMMANDS_CRUD = {"0": "0",
                 "1": "1",
                 "2": "2",
                 "3": "3",
                 "4": "4",
                 "5": "5"}

COMMANDS_TOP = {"0": "0",
                "1": "1",
                "2": "2",
                "3": "3"}

MAIN_MENU = """
MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria
"""

CRUD_MENU = """
CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies
"""

TOP_TEN_MENU = """
TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA
"""

# CRUD Menu functions
def create_company() -> None:
    print("Not implemented!")
    return None

def read_company() -> None:
    print("Not implemented!")
    return None

def update_company() -> None:
    print("Not implemented!")
    return None

def delete_company() -> None:
    print("Not implemented!")
    return None

def list_all_companies() -> None:
    print("Not implemented!")
    return None

# Top Ten Companies Menu functions
def list_ndn_ebitda() -> None:
    print("Not implemented!")
    return None

def list_roe() -> None:
    print("Not implemented!")
    return None

def list_roa() -> None:
    print("Not implemented!")
    return None

# CRUD MENU
def crud_menu() -> str|None:
    print(CRUD_MENU)

    crud_hub = user_input().lower()
    if crud_hub not in COMMANDS_CRUD:
        print("Invalid option!")
    else:
        match crud_hub:
            case "0":
                return "back"
            case "1":
                create_company()
                return "1"
            case "2":
                read_company()
                return "2"
            case "3":
                update_company()
                return "3"
            case "4":
                delete_company()
                return "4"
            case "5":
                list_all_companies()
                return "5"
            case _:
                print("Invalid input")
    return None

# TOP TEN MENU
def top_ten_menu() -> str|None:
    print(TOP_TEN_MENU)

    top_ten_hub = user_input().lower()
    if top_ten_hub not in COMMANDS_TOP:
        print("Invalid option!")
    else:
        match top_ten_hub:
            case "0":
                return "back"
            case "1":
                list_ndn_ebitda()
                return "1"
            case "2":
                list_roe()
                return "2"
            case "3":
                list_roa()
                return "3"
            case _:
                print("Invalid input")
    return None

# user input function
def user_input() -> str:
    choice = input("Enter an option:\n")
    return choice

# main loop
def main() -> None:

    while True:
        print(MAIN_MENU)

        user_choice = user_input().lower()
        if user_choice not in COMMANDS_MAIN:
            print("Invalid option!")
        else:
            match user_choice:
                case "0":
                    print("Have a nice day!\n")
                    break
                case "1":
                    crud_menu()
                case "2":
                    top_ten_menu()
                case _:
                    print("Invalid option!")

    return None

if __name__ == '__main__':
    main()