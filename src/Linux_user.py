import subprocess
import shlex


def list_users():
    list_command = "awk -F':' '{ print $1}' /etc/passwd"
    args = shlex.split(list_command)
    try:
        res = subprocess.run(args, capture_output=True, text=True)
        return res.stdout
    except subprocess.SubprocessError as e:
        print(f"an error {e} occurred ")


def create_user(username: str, password=None):
    add_user_command = f"sudo useradd {username}"
    if password:
        command = f"sudo useradd {username}"
        args = shlex.split(command)
        try:
            subprocess.run(args)
            subprocess.run(
                ["sudo", "chpasswd"],
                input=f"{username}:{password}",
                text=True,
                check=True
            )
            print(f"have created {username}")
        except subprocess.SubprocessError as e:
            print(f"an error {e} occurred ")
    else:
        args = shlex.split(add_user_command)
        try:
            subprocess.run(args,
                           check=True)
        except subprocess.SubprocessError as e:
            print(f"an error {e} occurred ")


def del_user(username: str):
    delete_user_command = f"sudo userdel {username}"
    args = shlex.split(delete_user_command)
    try:
        subprocess.run(args)
        print(f"have successfully deleted {username}")
    except subprocess.SubprocessError as e:
        print(f"an error {e} occurred")
