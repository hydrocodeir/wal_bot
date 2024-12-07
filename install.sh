#!/bin/bash

# Colors for better visuals
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check and install Python
echo -e "${GREEN}Checking Python installation...${NC}"
if ! command -v python3 &>/dev/null; then
    echo -e "${YELLOW}Python3 is not installed. Installing...${NC}"
    sudo apt update && sudo apt install -y python3 python3-pip || { echo -e "${RED}Failed to install Python3.${NC}"; exit 1; }
else
    echo -e "${CYAN}Python3 is already installed.${NC}"
fi

# Step 2: Check and install pip for Python3 if necessary
echo -e "${GREEN}Checking pip installation...${NC}"
if ! command -v pip3 &>/dev/null; then
    echo -e "${YELLOW}pip is not installed. Installing pip...${NC}"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3 get-pip.py || { echo -e "${RED}Failed to install pip.${NC}"; exit 1; }
else
    echo -e "${CYAN}pip is already installed.${NC}"
fi

# Step 3: Clone the repository
REPO_URL="https://github.com/primeZdev/wal_bot.git"
REPO_DIR="wal_bot"

echo -e "${GREEN}Cloning the wal_bot repository...${NC}"
if [ ! -d "$REPO_DIR" ]; then
    git clone "$REPO_URL" || { echo -e "${RED}Failed to clone the repository. Please check the URL or your internet connection.${NC}"; exit 1; }
else
    echo -e "${YELLOW}Repository already exists. Skipping clone step.${NC}"
fi

cd "$REPO_DIR" || { echo -e "${RED}Failed to enter the $REPO_DIR directory.${NC}"; exit 1; }

# Step 4: Prompt for configuration values
ENV_FILE=".env"

echo -e "${GREEN}Configuring your wal_bot...${NC}"

echo -e "${CYAN}Enter your Telegram Admin Chat ID:${NC} (example: 123456789)"
read -r ADMIN_CHAT_ID
ADMIN_CHAT_ID=${ADMIN_CHAT_ID:-123456789}

echo -e "${CYAN}Enter your Telegram Bot Token:${NC} (example: your_telegram_bot_token)"
read -r BOT_TOKEN
BOT_TOKEN=${BOT_TOKEN:-your_telegram_bot_token}

echo -e "${CYAN}Enter your Panel Address:${NC} (example: panel.example.com/path)"
read -r PANEL_ADDRESS
PANEL_ADDRESS=${PANEL_ADDRESS:-panel.example.com/fxg6JRgG6LqDjAG}

echo -e "${CYAN}Enter your Subscription Address:${NC} (example: panel.example.com/subpath)"
read -r SUB_ADDRESS
SUB_ADDRESS=${SUB_ADDRESS:-panel.example.com/sub}

echo -e "${CYAN}Enter your Panel Username:${NC} (example: your_panel_username)"
read -r PANEL_USER
PANEL_USER=${PANEL_USER:-your_panel_username}

echo -e "${CYAN}Enter your Panel Password:${NC} (example: your_panel_password)"
read -r PANEL_PASS
PANEL_PASS=${PANEL_PASS:-your_panel_password}

# Step 5: Save to .env file
cat <<EOF > "$ENV_FILE"
ADMIN_CHAT_ID=${ADMIN_CHAT_ID}
BOT_TOKEN=${BOT_TOKEN}
PANEL_ADDRESS=${PANEL_ADDRESS}
SUB_ADDRESS=${SUB_ADDRESS}
PANEL_USER=${PANEL_USER}
PANEL_PASS=${PANEL_PASS}
EOF

echo -e "${GREEN}Configuration saved successfully to ${ENV_FILE}!${NC}"

# Step 6: Install Python requirements using python3 -m pip
echo -e "${GREEN}Installing Python libraries...${NC}"
python3 -m pip install -r requirements.txt || { echo -e "${RED}Failed to install Python libraries. Please check your internet connection.${NC}"; exit 1; }

# Step 7: Run createdata.py one time
echo -e "${GREEN}Running createdata.py once...${NC}"
python3 createdata.py || { echo -e "${RED}Failed to run createdata.py. Please check for errors in the script.${NC}"; exit 1; }

# Step 8: Create a Systemd service
SERVICE_FILE="/etc/systemd/system/wal_bot.service"

sudo bash -c "cat <<EOF > ${SERVICE_FILE}
[Unit]
Description=wal_bot Telegram Bot Service
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

# Step 9: Enable and start the service
echo -e "${GREEN}Enabling and starting the wal_bot service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable wal_bot.service
sudo systemctl start wal_bot.service

echo -e "${GREEN}Your wal_bot is now running and configured to start on boot!${NC}"
