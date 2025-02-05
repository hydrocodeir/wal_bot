
# Change help message
def change_help_message(new_text):
    file_path = "src/messages/messages.py"

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    found = False 

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for line in lines:
                if line.startswith("HELP_MESSAGE"):
                    file.write(f'HELP_MESSAGE = """{new_text}"""\n')
                    found = True
                else:
                    file.write(line)

        return found
    
    except Exception as e:
        return False
