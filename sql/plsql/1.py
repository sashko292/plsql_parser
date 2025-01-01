import json
from antlr4 import FileStream, CommonTokenStream, ParserRuleContext
from Python3.PlSqlLexer import PlSqlLexer
from Python3.PlSqlParser import PlSqlParser
from Python3.PlSqlParserVisitor import PlSqlParserVisitor
from antlr4.tree.Tree import TerminalNode


class TableCollector(PlSqlParserVisitor):
    def __init__(self):
        self.table_info = {}  # Формат: {table_name: {"role": rule_name, "sources": set()}}

    def visitChildren(self, ctx):
        """
        Переопределённый метод для обработки всех детей узла.
        """
        if not ctx.children:
            return None
        return [self.visit(child) for child in ctx.children]

    def visit(self, ctx):
        """
        Переопределённый метод visit для обработки различных типов узлов дерева.
        """
        if isinstance(ctx, ParserRuleContext):  # Проверяем, что это контекст правила
            rule_name = PlSqlParser.ruleNames[ctx.getRuleIndex()]  # Получаем имя правила
            node = {
                "rule_name": rule_name,
                "text": ctx.getText(),
                "children": self.visitChildren(ctx)
            }
        elif isinstance(ctx, TerminalNode):  # Если это терминальный узел
            node = {
                "rule_name": None,  # У терминального узла нет имени правила
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
    input_stream = FileStream(file_path, encoding="utf-8")
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
    with open('output.json', 'w', encoding="utf-8") as json_file:
        json.dump(parsed_tree, json_file, ensure_ascii=False, indent=2)

    print("JSON сохранен в файл 'output.json'.")