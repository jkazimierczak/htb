import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from . import handlers
from inspect import getmembers, isfunction


def prompt(accounts: dict):
    functions = getmembers(handlers, isfunction)
    # func[0] is a function's name
    account_completer = WordCompleter(["exit", *[func[0] for func in functions]])
    session = PromptSession(completer=account_completer)

    print("Use TAB for autocompletion.")
    while True:
        try:
            command = session.prompt("htb account> ")
        except KeyboardInterrupt:
            print("Press CTRL+D to exit.")
            continue
        except EOFError:
            break

        # Find handler function and execute it
        if command == "exit":
            break
        found_handler = list(filter(lambda x: x[0] == command, functions))
        if not found_handler:
            print(f'Unknown command "{command}"')
            continue

        handler = found_handler[0][1]
        handler(accounts)

    return accounts
