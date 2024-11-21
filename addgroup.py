import json

def add_group(group_username):
    """
    Add a group username to the storage file.
    """
    try:
        with open("groups.json", "r") as file:
            groups = json.load(file)
    except FileNotFoundError:
        groups = []

    if group_username not in groups:
        groups.append(group_username)
        with open("groups.json", "w") as file:
            json.dump(groups, file, indent=4)
        print(f"Group '{group_username}' added successfully!")
    else:
        print(f"Group '{group_username}' is already added.")

if __name__ == "__main__":
    group_username = input("Enter the group username: ")
    add_group(group_username)
