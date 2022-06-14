from os.path import exists

TODOS = []


def is_confirmed(text):
    decision = input(f"{text} (y,n) : ")
    if decision.lower() == "y":
        return True
    return False


def add_todo():
    print("New Todo : ")
    text = input("Title : ")
    TODOS.append(text)
    print_todos()
    if is_confirmed("Add again?"):
        add_todo()


def print_todos():
    if len(TODOS) > 0:
        index = 0
        for item in TODOS:
            index += 1
            print(index, ". ", item)
    else:
        if is_confirmed("No TODOs added, Add one?"):
            add_todo()


def remove_todo():
    print_todos()
    option = int(input("Enter a number to remove : "))
    if option <= len(TODOS):
        del TODOS[option - 1]
        print_todos()
        if is_confirmed("Delete again?"):
            remove_todo()
    else:
        print("Invalid input")


def init():
    if exists("ToDo/data.txt"):
        data_file = open("ToDo/data.txt", "r")
        data = data_file.readlines()
        for line in data:
            TODOS.append(line.strip())
        data_file.close()


def save_file():
    data_file = open("ToDo/data.txt", "w")
    data_file.writelines(f"{line}\n" for line in TODOS)
    data_file.close()


def main():
    init()
    while True:
        print(
            """
        Welcome to TodoList

        1. View TODOs
        2. Add New TODO
        3. Remove TODO
        0. Exit
        """
        )
        option = int(input("Enter an option : "))
        if option == 0:
            break
        menus = {1: print_todos, 2: add_todo, 3: remove_todo}
        if menus.keys().__contains__(option):
            menus[option]()
        else:
            print("Invalid Option")
    save_file()


main()
