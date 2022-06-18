from curses.ascii import isdigit
from datetime import datetime
from os.path import exists

TODOS = []


def invalid_error():
    print("Invalid Input")


def is_confirmed(text):
    decision = input(f"{text} (y,n) : ")
    if decision.lower() == "y":
        return True
    return False


def valid_date_by_month(year):
    return {
        1: 31,
        2: 29 if (int(year) % 4 == 0) else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }


def is_valid_date(str):
    if str == "0":
        return False
    if len(str.split("-")) != 3:
        invalid_error()
        return False
    for part in str.split("-"):
        if not part.isdigit():
            invalid_error()
            return False
    year, month, day = [int(x) for x in str.split("-")]
    if (
        year in range(1970, 3000)
        and month in range(1, 13)
        and (day in range(1, 1 + valid_date_by_month(year)[month]))
    ):
        return True
    invalid_error()
    return False


def is_valid_time(str):
    if str == "0":
        return False
    parts = str.split(":")
    if len(parts) != 2:
        invalid_error()
        return False
    for part in parts:
        if not part.isdigit():
            invalid_error()
            return False
    hour, minute = [int(x) for x in str.split(":")]
    if hour in range(0, 24) and minute in range(0, 60):
        return True
    invalid_error()
    return False


def get_datetime(dateStr, timeStr):
    if is_valid_date(dateStr) and is_valid_time(timeStr):
        year, month, day = [int(x) for x in dateStr.split("-")]
        hour, minute = [int(x) for x in timeStr.split(":")]
        return datetime(year, month, day, hour, minute)
    return None


def has_time_clash(time):
    for item in TODOS:
        if int(time.timestamp() * 1000) in range(
            int(item["start_time"] * 1000), int(item["end_time"] * 1000) + 1
        ):
            return True
    return False


def add_todo():
    print("New Todo : ")
    description = input("Descriotion : ")
    startDateStr = "0"
    while not is_valid_date(startDateStr):
        startDateStr = input("Start Date : ")
    startTimeStr = "0"
    while not is_valid_time(startTimeStr):
        startTimeStr = input("Start Time : ")
    if has_time_clash(get_datetime(startDateStr, startTimeStr)):
        print("You have another todo at the same time, starting over...")
        add_todo()
        return
    endDateStr = "0"
    while not is_valid_date(endDateStr):
        endDateStr = input("End Date : ")
    endTimeStr = "0"
    while not is_valid_time(endTimeStr):
        endTimeStr = input("End Time : ")
    if has_time_clash(get_datetime(endDateStr, endTimeStr)):
        print("You have another todo at the same time, starting over...")
        add_todo()
        return
    place = input("Place : ")
    TODOS.append(
        {
            "description": description,
            "place": place,
            "start_time": get_datetime(startDateStr, startTimeStr).timestamp(),
            "end_time": get_datetime(endDateStr, endTimeStr).timestamp(),
        }
    )
    print_todos()
    if is_confirmed("Add again?"):
        add_todo()


def print_todos():
    if len(TODOS) > 0:
        index = 0
        for item in TODOS:
            index += 1
            print("\n", index, ". ")
            print(item["description"])
            print("Start : ", datetime.fromtimestamp(item["start_time"]))
            print("End : ", datetime.fromtimestamp(item["end_time"]))
            print("Place : ", item["place"], "\n")
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
            if len(line.split("|")) == 4:
                description, place, start_time, end_time = line.strip().split("|")
                TODOS.append(
                    {
                        "description": description,
                        "place": place,
                        "start_time": float(start_time),
                        "end_time": float(end_time),
                    }
                )
        data_file.close()


def save_file():
    data_file = open("ToDo/data.txt", "w")
    data_file.writelines(
        f'{("|".join((str(item[key]) for key in item)))}\n' for item in TODOS
    )
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

# init()
# print_todos()
# print(has_time_clash(get_datetime("2022-03-18", "12:42")))
