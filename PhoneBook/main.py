from os.path import exists

CONTACTS = []


def init():
    if exists("PhoneBook/data.txt"):
        data_file = open("PhoneBook/data.txt", "r")
        data = data_file.readlines()
        for line in data:
            if len(line.split("|")) >= 3:
                name, address, email, *phones = line.strip().split("|")
                CONTACTS.append(
                    {
                        "name": name,
                        "address": address,
                        "email": email,
                        "phones": phones,
                    }
                )
        data_file.close()


def save_file():
    data_file = open("PhoneBook/data.txt", "w")
    data_file.writelines(
        f'{("|".join((str(item[key]) for key in item if key != "phones")))}|{"|".join(phone for phone in item["phones"])}\n'
        for item in CONTACTS
    )
    data_file.close()


def main():
    print(
        """
    Welcome to PhoneBook
    """
    )


init()
print(CONTACTS)
save_file()
