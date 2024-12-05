#!/bin/bash

# Colors for better visuals
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Clone the repository
echo -e "${GREEN}Cloning the wal_bot repository...${NC}"
if [ -d "wal_bot" ]; then
    echo -e "${YELLOW}The wal_bot directory already exists. Skipping cloning.${NC}"
else
    git clone https://github.com/primeZdev/wal_bot.git || {
        echo -e "${RED}Failed to clone the wal_bot repository. Please check your internet connection or repository URL.${NC}"
        exit 1
    }
    cd wal_bot || { echo -e "${RED}Failed to enter the wal_bot directory.${NC}"; exit 1; }
fi

# Step 2: Function to ask for user input
prompt_input() {
    local var_name="$1"
    local var_desc="$2"
    local default_value="$3"
    local input_value

    while true; do
        echo -e "${CYAN}${var_desc}${NC} [${YELLOW}${default_value}${NC}]: "
        read -r input_value
        if [ -n "$input_value" ] || [ -n "$default_value" ]; then
            echo "${input_value:-$default_value}"
            break
        else
            echo -e "${RED}This field cannot be empty. Please provide a value.${NC}"
        fi
    done
}

# Step 3: Configuration
ENV_FILE=".env"

echo -e "${GREEN}Configuring your wal_bot...${NC}"
if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}.env already exists. Do you want to overwrite it? (y/n)${NC}"
    read -r overwrite
    if [ "$overwrite" != "y" ]; then
        echo -e "${YELLOW}Skipping configuration.${NC}"
        exit 0
    fi
fi

ADMIN_CHAT_ID=$(prompt_input "ADMIN_CHAT_ID" "Enter your Telegram Admin Chat ID" "123456789")
BOT_TOKEN=$(prompt_input "BOT_TOKEN" "Enter your Telegram Bot Token" "your_telegram_bot_token")
PANEL_ADDRESS=$(prompt_input "PANEL_ADDRESS" "Enter your Panel Address" "panel.example.com/fxg6JRgG6LqDjAG")
SUB_ADDRESS=$(prompt_input "SUB_ADDRESS" "Enter your Subscription Address" "panel.example.com/sub")
PANEL_USER=$(prompt_input "PANEL_USER" "Enter your Panel Username" "your_panel_username")
PANEL_PASS=$(prompt_input "PANEL_PASS" "Enter your Panel Password" "your_panel_password")

# Step 4: Save configuration to .env
echo -e "${GREEN}Saving configuration to ${ENV_FILE}...${NC}"
cat <<EOF > "$ENV_FILE"
ADMIN_CHAT_ID=${ADMIN_CHAT_ID}
BOT_TOKEN=${BOT_TOKEN}
PANEL_ADDRESS=${PANEL_ADDRESS}
SUB_ADDRESS=${SUB_ADDRESS}
PANEL_USER=${PANEL_USER}
PANEL_PASS=${PANEL_PASS}
EOF

echo -e "${GREEN}Configuration saved successfully!${NC}"

# Step 5: Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
sudo apt update && sudo apt install -y python3 python3-pip git

# Step 6: Install Python requirements
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}requirements.txt not found. Please ensure the file exists in the wal_bot repository.${NC}"
    exit 1
fi
echo -e "${GREEN}Installing Python libraries...${NC}"
pip3 install -r requirements.txt

# Step 7: Create a Systemd service
SERVICE_FILE="/etc/systemd/system/wal_bot.service"

echo -e "${GREEN}Creating a Systemd service for wal_bot...${NC}"
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

# Step 8: Enable and start the service
echo -e "${GREEN}Enabling and starting the wal_bot service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable wal_bot.service
sudo systemctl start wal_bot.service

# Step 9: Check the service status
if sudo systemctl is-active --quiet wal_bot.service; then
    echo -e "${GREEN}wal_bot service is running successfully!${NC}"
else
    echo -e "${RED}Failed to start wal_bot service. Check the logs using 'sudo journalctl -u wal_bot'.${NC}"
fi

echo -e "${GREEN}Your wal_bot is now running and configured to start on boot!${NC}"
