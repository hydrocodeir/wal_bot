
set -e


CYAN='\e[36m'
GREEN='\e[32m'
YELLOW='\e[33m'
RED='\e[31m'
NC='\e[0m'
INSTALL_DIR="/opt/walbot"

install_wal_bot() {
    echo -e "${GREEN}Installing Wal Bot...${NC}"
    sudo apt update && sudo apt upgrade -y
    curl -fsSL https://get.docker.com | sh
    sudo mkdir -p "$INSTALL_DIR/data"
    sudo curl -o "$INSTALL_DIR/docker-compose.yml" https://raw.githubusercontent.com/primeZdev/wal_bot/main/docker-compose.yml
    cd "$INSTALL_DIR"
    sudo curl -o .env https://raw.githubusercontent.com/primeZdev/wal_bot/main/.env.example
    sudo nano .env
    sudo docker compose up -d
    echo -e "${GREEN}Wal Bot installed successfully!${NC}"
}

update_wal_bot() {
    echo -e "${YELLOW}Updating Wal Bot...${NC}"
    cd "$INSTALL_DIR"
    cd /opt/walbot
    sudo docker compose pull && docker compose up -d
    echo -e "${GREEN}Wal Bot updated successfully!${NC}"
}

remove_wal_bot() {
    echo -e "${RED}Removing Wal Bot...${NC}"
    cd "$INSTALL_DIR"
    sudo docker compose down
    sudo rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}Wal Bot removed successfully!${NC}"
}

while true; do
    clear
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}      Wal Bot Installer  |  @primez_dev ${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo -e "${GREEN} 1.   Install Wal Bot${NC}"
    echo -e "${YELLOW} 2.   Update Wal Bot${NC}"
    echo -e "${RED} 3.   Remove Wal Bot${NC}"
    echo -e "${CYAN} 4.   Exit${NC}"
    echo -e "${CYAN}========================================${NC}"
    read -rp "👉 Choose an option: " OPTION
    case $OPTION in
        1) install_wal_bot ;;
        2) update_wal_bot ;;
        3) remove_wal_bot ;;
        4) echo -e "${CYAN}Goodbye!  ${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ;;
    esac
    sleep 2
done
