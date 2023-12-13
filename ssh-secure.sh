#!/bin/bash
red='\033[0;31m'
bblue='\033[0;34m'
yellow='\033[0;33m'
green='\033[0;32m'
plain='\033[0m'
red(){ echo -e "\033[31m\033[01m$1\033[0m";}
green(){ echo -e "\033[32m\033[01m$1\033[0m";}
yellow(){ echo -e "\033[33m\033[01m$1\033[0m";}
blue(){ echo -e "\033[36m\033[01m$1\033[0m";}
white(){ echo -e "\033[37m\033[01m$1\033[0m";}
bblue(){ echo -e "\033[34m\033[01m$1\033[0m";}
rred(){ echo -e "\033[35m\033[01m$1\033[0m";}
readtp(){ read -t5 -n26 -p "$(yellow "$1")" $2;}
readp(){ read -p "$(yellow "$1")" $2;}

install_fail2ban() {
    sudo apt-get update
    sudo apt-get install fail2ban -y
}

configure_fail2ban() {
    sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
    sudo sed -i '/^\[sshd\]/,/^\[/ s/^enabled = .*/enabled = true/' /etc/fail2ban/jail.local
    sudo sed -i '/^\[sshd\]/,/^\[/ s/^port = .*/port = ssh/' /etc/fail2ban/jail.local
    sudo sed -i '/^\[sshd\]/,/^\[/ s/^filter = .*/filter = sshd/' /etc/fail2ban/jail.local
    sudo sed -i '/^\[sshd\]/,/^\[/ s|^logpath = .*|logpath = /var/log/auth.log|' /etc/fail2ban/jail.local
    sudo sed -i '/^\[sshd\]/,/^\[/ s/^maxretry = .*/maxretry = 3/' /etc/fail2ban/jail.local
    sudo sed -i '/^\[sshd\]/,/^\[/ s/^bantime = .*/bantime = 360000/' /etc/fail2ban/jail.local
    sudo systemctl restart fail2ban
}

check_fail2ban_status() {
    sudo systemctl status fail2ban
}

configure_ssh() {
    sshd_config="/etc/ssh/sshd_config"
    #sudo sed -i 's/^PermitRootLogin .*/PermitRootLogin no/' $sshd_config
    sudo sed -i 's/^PasswordAuthentication .*/PasswordAuthentication no/' $sshd_config
    sudo sed -i 's/^ChallengeResponseAuthentication .*/ChallengeResponseAuthentication no/' $sshd_config
    sudo sed -i 's/^UsePAM .*/UsePAM no/' $sshd_config
    sudo systemctl restart ssh
}

create_and_copy_ssh_key() {
    ssh-keygen -t rsa -b 2048
    readp "Enter the server IP: " server_ip
    readp "Enter the SSH port (default is 22): " ssh_port
    ssh_port=${ssh_port:-22}
    ssh-copy-id -p $ssh_port user@$server_ip
}

yellow "------------------Choose an option--------------------"
green "1. Local Machine (Generate SSH key and copy to server)"
green "2. Server (Install Fail2Ban and configure SSH)"
white "------------------------------------------------------"
readp "Enter your choice (1 or 2): " choice

case $choice in
    1)
        create_and_copy_ssh_key
        ;;
    2)
        if ! command -v fail2ban &> /dev/null; then
            yellow "Installing Fail2Ban..."
            install_fail2ban
            configure_fail2ban
        else
            yellow "Fail2Ban is already installed."
            check_fail2ban_status
        fi

        yellow "Configuring SSH..."
        configure_ssh
        ;;
    *)
        red "Invalid choice. Exiting."
        exit 1
        ;;
esac

bblue "Setup complete."
