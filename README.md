# random-tools
Here are some random tools I created for personal use, I thought it might be useful for others too!

## type-mover.py
A simple Python script that asks you for a directory and file type that you want to delete then proceeds to move all matching files in all subdirectories to the folder type_files. It can also reverse the process.
```bash
python3 <(curl -sL https://raw.githubusercontent.com/hrostami/random-tools/main/type_mover.py)
```
## ssh-secure.sh
A shell script to setup fail2ban on your server and configure ssh to not use password authentication and use ssh key instead. Also you can create ssh key on your local machine and copy it to the server using this script.
```bash
bash <(curl -sL https://raw.githubusercontent.com/hrostami/random-tools/main/ssh-secure.sh)
```
