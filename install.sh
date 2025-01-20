#!/bin/bash

# Colors for better visuals
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function: Install wal_bot
install_wal_bot() {
    echo -e "${GREEN}Starting installation process...${NC}"
    
    # Step 1: Check and install Python
    echo -e "${GREEN}Checking Python installation...${NC}"
    if ! command -v python3 &>/dev/null; then
        echo -e "${YELLOW}Python3 is not installed. Installing...${NC}"
        sudo apt update && sudo apt install -y python3 || { echo -e "${RED}Failed to install Python3.${NC}"; exit 1; }
    else
        echo -e "${CYAN}Python3 is already installed.${NC}"
    fi

    # Step 2: Install pip if not available
    if ! command -v pip3 &>/dev/null; then
        echo -e "${YELLOW}pip3 is not installed. Installing...${NC}"
        sudo apt install -y python3-pip || { echo -e "${RED}Failed to install pip3.${NC}"; exit 1; }
    else
        echo -e "${CYAN}pip3 is already installed.${NC}"
    fi

    # Step 3: Clone or update the repository
    REPO_URL="https://github.com/primeZdev/wal_bot.git"
    REPO_DIR="wal_bot"
    if [ ! -d "$REPO_DIR" ]; then
        echo -e "${GREEN}Cloning the wal_bot repository...${NC}"
        git clone "$REPO_URL" || { echo -e "${RED}Failed to clone the repository.${NC}"; exit 1; }
    else
        echo -e "${YELLOW}Repository already exists. Updating...${NC}"
        cd "$REPO_DIR" && git pull || { echo -e "${RED}Failed to update the repository.${NC}"; exit 1; }
        cd ..
    fi

    cd "$REPO_DIR" || { echo -e "${RED}Failed to enter the repository directory.${NC}"; exit 1; }

    # Step 4: Prompt for configuration values
    ENV_FILE=".env"
    echo -e "${GREEN}Configuring your wal_bot...${NC}"

    read -rp "$(echo -e "${CYAN}Enter your Telegram Admin Chat ID: ${NC}")" ADMIN_CHAT_ID
    read -rp "$(echo -e "${CYAN}Enter your Telegram Bot Token: ${NC}")" BOT_TOKEN
    read -rp "$(echo -e "${CYAN}Enter your Panel Address example, panel.example.com:port/fLqjAG: ${NC}")" PANEL_ADDRESS
    read -rp "$(echo -e "${CYAN}Enter your Subscription Address example, panel.example.com:port/sub: ${NC}")" SUB_ADDRESS
    read -rp "$(echo -e "${CYAN}Enter your Panel Username: ${NC}")" PANEL_USER
    read -rp "$(echo -e "${CYAN}Enter your Panel Password: ${NC}")" PANEL_PASS

    cat <<EOF > "$ENV_FILE"
ADMIN_CHAT_ID=${ADMIN_CHAT_ID}
BOT_TOKEN=${BOT_TOKEN}
PANEL_ADDRESS=${PANEL_ADDRESS}
SUB_ADDRESS=${SUB_ADDRESS}
PANEL_USER=${PANEL_USER}
PANEL_PASS=${PANEL_PASS}
EOF

    echo -e "${GREEN}Configuration saved successfully to ${ENV_FILE}!${NC}"

    # Step 5: Install Python requirements
    echo -e "${GREEN}Installing Python libraries...${NC}"
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt || { echo -e "${RED}Failed to install Python libraries.${NC}"; exit 1; }

    # Step 6: Create a Systemd service
    SERVICE_FILE="/etc/systemd/system/wal_bot.service"
    sudo bash -c "cat <<EOF > ${SERVICE_FILE}
[Unit]
Description=wal_bot
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

    # Step 7: Enable and start the service
    echo -e "${GREEN}Enabling and starting the wal_bot service...${NC}"
    sudo systemctl daemon-reload
    sudo systemctl enable wal_bot.service
    sudo systemctl start wal_bot.service || { echo -e "${RED}Failed to start the wal_bot service.${NC}"; exit 1; }

    echo -e "${GREEN}Your wal_bot is now running and configured to start on boot!${NC}"
}


# Function: Update wal_bot
update_wal_bot() {
    echo -e "${GREEN}Updating wal_bot...${NC}"
    REPO_DIR="wal_bot"
    if [ -d "$REPO_DIR" ]; then
        cd "$REPO_DIR" || { echo -e "${RED}Failed to enter the repository directory.${NC}"; exit 1; }
        git pull || { echo -e "${RED}Failed to update the repository.${NC}"; exit 1; }
        python3 -m pip install -r requirements.txt || { echo -e "${RED}Failed to update Python libraries.${NC}"; exit 1; }
        sudo systemctl restart wal_bot.service
        echo -e "${GREEN}wal_bot updated successfully!${NC}"
    else
        echo -e "${RED}Repository not found. Please install first.${NC}"
    fi
}

# Function: Remove wal_bot
remove_wal_bot() {
    echo -e "${RED}Removing wal_bot...${NC}"
    sudo systemctl stop wal_bot.service
    sudo systemctl disable wal_bot.service
    sudo rm -rf wal_bot /etc/systemd/system/wal_bot.service
    sudo systemctl daemon-reload
    echo -e "${RED}wal_bot has been removed!${NC}"
}

# Main menu
while true; do
    echo -e "\n${CYAN}==== Wal Bot Manager ====${NC}"
    echo -e "${GREEN}1. Install wal bot${NC}"
    echo -e "${YELLOW}2. Update wal bot${NC}"
    echo -e "${RED}3. Remove wal bot${NC}"
    echo -e "${CYAN}4. Exit${NC}"
    read -rp "Choose an option: " OPTION

    case $OPTION in
        1) install_wal_bot ;;
        2) update_wal_bot ;;
        3) remove_wal_bot ;;
        4) echo -e "${CYAN}Exiting...${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ;;
    esac
done
