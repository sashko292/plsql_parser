import os

def fix_generated_files(directory):
    files_to_fix = ["PlSqlLexer.py", "PlSqlParser.py"]
    for file_name in files_to_fix:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                content = file.read()
            
            # Заменяем 'this' на 'self'
            content = content.replace("this.", "self.")
            
            with open(file_path, "w") as file:
                file.write(content)
            print(f"Fixed file: {file_name}")
        else:
            print(f"File not found: {file_name}")

if __name__ == "__main__":
    # Укажите путь к папке с сгенерированными файлами
    directory = "/Users/sashko/Documents/GitHub/grammars-v4/sql/plsql"
    fix_generated_files(directory)