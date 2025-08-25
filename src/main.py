import os
import argparse
import windows_user as wu
import Linux_user as lu

cli = argparse.ArgumentParser("This is a CLI user/app manager")
cli.add_argument("-A", "--Auto", action="store_true", help="Interactive mode with menu loop")
cli.add_argument("-L", "--List", action="store_true", help="List all users on the system")
cli.add_argument("-U", "--Username", type=str, help="Username to create or delete")
cli.add_argument("-p", "--Password", type=str, help="Password for the user")
cli.add_argument("-D", "--Delete", action="store_true", help="Delete the given user")

args = cli.parse_args()


def is_windows():
    return os.name == "nt"


if __name__ == "__main__":
    if args.Auto:
        # Interactive loop
        option_map = {"1": "list users", "2": "add user", "3": "del user", "4": "exit"}
        while True:
            for k, v in option_map.items():
                print(f"{k}. {v}")
            choice = input("Enter an option: ")

            if choice == "1":
                wu.enumerate_users() if is_windows() else lu.list_users()

            elif choice == "2":
                username = input("Enter a username: ")
                password = input("Enter a password: ")
                if is_windows():
                    wu.add_user(username, password)
                else:
                    lu.create_user(username, password)

            elif choice == "3":
                username = input("Enter username to delete: ")
                if is_windows():
                    wu.delete_user(username)
                else:
                    lu.del_user(username)

            elif choice == "4":
                print("Exiting program.")
                break

            else:
                print("Invalid option.")

    else:
        if args.List:
            wu.enumerate_users() if is_windows() else lu.list_users()

        if args.Username and not args.Delete:
            if is_windows():
                wu.add_user(args.Username, args.Password)
            else:
                lu.create_user(args.Username, args.Password)

        if args.Username and args.Delete:
            if is_windows():
                wu.delete_user(args.Username)
            else:
                lu.del_user(args.Username)
