import json
from antlr4 import FileStream, CommonTokenStream, ParserRuleContext
from Python3.PlSqlLexer import PlSqlLexer
from Python3.PlSqlParser import PlSqlParser
from Python3.PlSqlParserVisitor import PlSqlParserVisitor
from antlr4.tree.Tree import TerminalNode


class TableCollector(PlSqlParserVisitor):
    def __init__(self):
        self.table_info = {}  # Формат: {table_name: {"role": rule_name, "sources": set()}}

    def visit(self, ctx):
        """
        Переопределённый метод visit для обработки различных типов узлов дерева.
        """
        # Проверяем, является ли узел парсером правил или терминальным узлом
        if isinstance(ctx, ParserRuleContext):  # Правильный класс для парсеров
            node = {
                "rule_name": ctx.getRuleIndex(),
                "text": ctx.getText(),
                "children": [self.visit(c) for c in ctx.children] if ctx.children else []
            }
        elif isinstance(ctx, TerminalNode):  # Для терминальных узлов
            node = {
                "rule_name": None,  # Для терминальных узлов у нас нет rule_name
                "text": ctx.getText(),
                "children": []
            }
        else:
            node = {
                "rule_name": "unknown",
                "text": "unknown",
                "children": []
            }

        return node

    def get_table_info(self):
        """
        Возвращает информацию о таблицах с их ролями и источниками.
        """
        return self.table_info


def parse_plsql(file_path):
    """
    Парсит PL/SQL файл.
    """
    input_stream = FileStream(file_path)
    lexer = PlSqlLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PlSqlParser(token_stream)

    # Разбираем дерево
    tree = parser.sql_script()
    collector = TableCollector()
    parsed_tree = collector.visit(tree)
    return parsed_tree


if __name__ == "__main__":
    # Укажите путь к вашему SQL-файлу
    file_path = "/Users/sashko/Documents/GitHub/grammars-v4/sql/plsql/load_data.sql"

    # Парсинг и получение дерева разбора
    parsed_tree = parse_plsql(file_path)

    # Сохранение дерева в файл output.json
    with open('output.json', 'w') as json_file:
        json.dump(parsed_tree, json_file, indent=2)

    print("JSON сохранен в файл 'output.json'.")