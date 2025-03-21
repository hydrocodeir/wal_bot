set -e

CYAN='\e[36m'
GREEN='\e[32m'
YELLOW='\e[33m'
RED='\e[31m'
NC='\e[0m'
INSTALL_DIR="/opt/walbot"
DONATION_ADDRESS="TBmQbMVGLer2DkX4RUmuunAYR73nzAtjYL"

print_progress() {
    local title=$1
    echo -e "\n${CYAN}$title${NC}\n"
}

print_step() {
    local step=$1
    local message=$2
    echo -e "${YELLOW}[$step]${NC} ⇾  ${message}"
}

print_success() {
    local message=$1
    echo -e "\n${GREEN}✓ ${message}${NC}\n"
}

print_error() {
    local message=$1
    echo -e "\n${RED}✗ ${message}${NC}\n"
}

install_wal_bot() {
    print_progress "INSTALLING WALBOT"
    
    print_step "1/7" "Updating packages..."
    sudo apt update && sudo apt upgrade -y || { print_error "Failed to update packages"; return 1; }
    
    print_step "2/7" "Installing Docker..."
    curl -fsSL https://get.docker.com | sh || { print_error "Failed to install Docker"; return 1; }
    
    print_step "3/7" "Creating directories..."
    sudo mkdir -p "$INSTALL_DIR/data" || { print_error "Failed to create directories"; return 1; }
    
    print_step "4/7" "Downloading config files..."
    sudo curl -o "$INSTALL_DIR/docker-compose.yml" https://raw.githubusercontent.com/primeZdev/wal_bot/main/docker-compose.yml
    cd "$INSTALL_DIR"
    sudo curl -o .env.example https://raw.githubusercontent.com/primeZdev/wal_bot/main/.env.example
    
    print_step "5/7" "Setting up BOT configuration..."
    echo -e "${CYAN}Please enter your Telegram Bot Token:${NC}"
    read -r BOT_TOKEN
    
    echo -e "${CYAN}Please enter your Telegram Admin Chat ID:${NC}"
    read -r ADMIN_CHAT_ID
    
    print_step "6/7" "Creating .env file..."
    sed "s/BOT_TOKEN=.*/BOT_TOKEN=$BOT_TOKEN/" .env.example > .env
    sed -i "s/ADMIN_CHAT_ID=.*/ADMIN_CHAT_ID=$ADMIN_CHAT_ID/" .env
    
    print_step "7/7" "Starting services..."
    sudo docker compose up -d || { print_error "Failed to start services"; return 1; }
    
    print_success "Wal Bot installed successfully!"
}

update_wal_bot() {
    print_progress "UPDATING WALBOT"
    
    cd "$INSTALL_DIR" || { print_error "Installation directory not found"; return 1; }
    
    print_step "1/4" "Pulling latest changes..."
    sudo docker compose pull || { print_error "Failed to pull updates"; return 1; }
    
    print_step "2/4" "Starting services..."
    sudo docker compose up -d || { print_error "Failed to start services"; return 1; }
    
    print_step "3/4" "Running database migrations..."
    sudo docker exec walbot-walbot-1 alembic upgrade head || { print_error "Failed to run migrations"; return 1; }
    
    print_step "4/4" "Restarting services..."
    sudo docker compose restart || { print_error "Failed to restart services"; return 1; }
    
    print_success "Wal Bot updated successfully!"
}

remove_wal_bot() {
    print_progress "REMOVING WALBOT"
    
    print_step "1/2" "Stopping services..."
    cd "$INSTALL_DIR" && sudo docker compose down || { print_error "Failed to stop services"; return 1; }
    
    print_step "2/2" "Removing files..."
    sudo rm -rf "$INSTALL_DIR" || { print_error "Failed to remove files"; return 1; }
    
    print_success "Wal Bot removed successfully!"
}

show_donation() {
    print_progress "SUPPORT WAL BOT DEVELOPMENT"
    
    echo -e "${GREEN}Thank you for considering a donation!${NC}"
    echo -e "Your support helps keep this project alive and improving."
    echo -e ""
    echo -e "${BLUE}TRON network(TRC20):${NC}"
    echo -e "${YELLOW}$DONATION_ADDRESS${NC}"
    echo -e ""
    echo -e "You can copy it."
    echo -e "${CYAN}Feel free to reach out to @primez_dev with any suggestions!${NC}"
    
    print_success "Thank you for your support!"
}

show_menu() {
    echo -e "${CYAN}WALBOT INSTALLER${NC}"
    echo -e "${CYAN}@primez_dev${NC}"
    echo -e ""
    echo -e "${GREEN}1.${NC} Install WalBot"
    echo -e "${YELLOW}2.${NC} Update WalBot"
    echo -e "${RED}3.${NC} Remove WalBot"
    echo -e "${BLUE}4.${NC} Donate"
    echo -e "${CYAN}4.${NC} Exit"
    echo -e ""
    echo -e "${CYAN}[?]${NC} Choose an option (1-4): "
}

while true; do
    clear
    show_menu
    read -r OPTION
    case $OPTION in
        1) install_wal_bot ;;
        2) update_wal_bot ;;
        3) remove_wal_bot ;;
        4) show_donation ;;
        4) echo -e "\n${CYAN}Goodbye! ${NC}\n"; exit 0 ;;
        *) echo -e "\n${RED}Invalid option. Please try again.${NC}\n" ;;
    esac
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read -r
done
