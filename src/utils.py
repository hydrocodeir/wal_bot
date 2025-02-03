
# Change help message
def change_help_message(filename, var_name, new_text):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            if line.startswith(var_name):
                file.write(f'{var_name} = """{new_text}"""\n')
            else:
                file.write(line)
