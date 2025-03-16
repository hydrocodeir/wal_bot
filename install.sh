set -e


CYAN='\e[36m'
GREEN='\e[32m'
YELLOW='\e[33m'
RED='\e[31m'
NC='\e[0m'
INSTALL_DIR="/opt/walbot"

print_progress() {
    local title=$1
    local title_length=${#title}
    local padding_size=$(( (40 - title_length) / 2 ))
    local padding=$(printf '%*s' "$padding_size" '')
    
    echo -e "\n${CYAN}┌────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC}${padding}${title}${padding}${CYAN}│${NC}"
    echo -e "${CYAN}└────────────────────────────────────────────┘${NC}\n"
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
    
    print_step "1/6" "Updating packages..."
    sudo apt update && sudo apt upgrade -y || { print_error "Failed to update packages"; return 1; }
    
    print_step "2/6" "Installing Docker..."
    curl -fsSL https://get.docker.com | sh || { print_error "Failed to install Docker"; return 1; }
    
    print_step "3/6" "Creating directories..."
    sudo mkdir -p "$INSTALL_DIR/data" || { print_error "Failed to create directories"; return 1; }
    
    print_step "4/6" "Downloading config files..."
    sudo curl -o "$INSTALL_DIR/docker-compose.yml" https://raw.githubusercontent.com/primeZdev/wal_bot/main/docker-compose.yml
    cd "$INSTALL_DIR"
    sudo curl -o .env https://raw.githubusercontent.com/primeZdev/wal_bot/main/.env.example
    
    print_step "5/6" "Setting up configuration..."
    echo -e "${CYAN}Please edit the .env file...${NC}"
    sudo nano .env
    
    print_step "6/6" "Starting services..."
    sudo docker compose up -d || { print_error "Failed to start services"; return 1; }
    
    print_success "Wal Bot installed successfully!"
}

update_wal_bot() {
    print_progress "UPDATING WALBOT"
    
    cd "$INSTALL_DIR" || { print_error "Installation directory not found"; return 1; }
    
    print_step "1/3" "Pulling latest changes..."
    sudo docker compose pull || { print_error "Failed to pull updates"; return 1; }
    
    print_step "2/3" "Starting services..."
    sudo docker compose up -d || { print_error "Failed to start services"; return 1; }
    
    # print_step "3/4" "Running database migrations..."
    # sudo docker exec walbot-walbot-1 alembic upgrade head || { print_error "Failed to run migrations"; return 1; }
    
    print_step "3/3" "Restarting services..."
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

show_menu() {
    echo -e "${CYAN}┌────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC}            WALBOT INSTALLER                ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}             @primez_dev                    ${CYAN}│${NC}"
    echo -e "${CYAN}├────────────────────────────────────────────┤${NC}"
    echo -e "${CYAN}│${NC}    ${GREEN}1.${NC} Install WalBot                      ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}    ${YELLOW}2.${NC} Update WalBot                       ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}    ${RED}3.${NC} Remove WalBot                       ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}    ${CYAN}4.${NC} Exit                                 ${CYAN}│${NC}"
    echo -e "${CYAN}└────────────────────────────────────────────┘${NC}"
    echo -e "\n${CYAN}[?]${NC} Choose an option (1-4): "
}

while true; do
    clear
    show_menu
    read -r OPTION
    case $OPTION in
        1) install_wal_bot ;;
        2) update_wal_bot ;;
        3) remove_wal_bot ;;
        4) echo -e "\n${CYAN}Goodbye! ${NC}\n"; exit 0 ;;
        *) echo -e "\n${RED}Invalid option. Please try again.${NC}\n" ;;
    esac
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read -r
done
