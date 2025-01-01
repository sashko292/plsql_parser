import os
from antlr4 import FileStream, CommonTokenStream
from Python3.PlSqlLexer import PlSqlLexer
from Python3.PlSqlParser import PlSqlParser
from Python3.PlSqlParserVisitor import PlSqlParserVisitor


class PlSqlDependencyVisitor(PlSqlParserVisitor):
    def __init__(self):
        self.source_tables = set()
        self.target_tables = set()
        self.columns = set()

    def visitTable_name(self, ctx):
        """Извлечение таблиц."""
        table_name = ctx.getText()
        parent_rule = ctx.parentCtx.getRuleIndex() if ctx.parentCtx else None
        rule_name = ctx.parser.ruleNames[parent_rule] if parent_rule is not None else None

        if rule_name in ("dml_table_expression_clause", "insert_into_clause"):
            self.target_tables.add(table_name)  # Таблица-потребитель
        else:
            self.source_tables.add(table_name)  # Таблица-источник

        return self.visitChildren(ctx)

    def visitColumn_name(self, ctx):
        """Извлечение колонок."""
        column_name = ctx.getText()
        self.columns.add(column_name)
        return self.visitChildren(ctx)

    def get_dependencies(self):
        """Возврат всех найденных зависимостей."""
        return {
            "source_tables": self.source_tables,
            "target_tables": self.target_tables,
            "columns": self.columns,
        }


def parse_plsql(file_path):
    """Функция для парсинга PL/SQL файла."""
    input_stream = FileStream(file_path)
    lexer = PlSqlLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PlSqlParser(token_stream)

    # Начальное правило грамматики
    tree = parser.sql_script()

    # Обход дерева разбора
    visitor = PlSqlDependencyVisitor()
    visitor.visit(tree)
    return visitor.get_dependencies()


if __name__ == "__main__":
    # Укажите путь к вашему SQL-файлу
    file_path = os.path.join(
        "/Users/sashko/Documents/GitHub/grammars-v4/sql/plsql", "load_data.sql"
    )

    # Парсинг и вывод зависимостей
    dependencies = parse_plsql(file_path)
    print("Dependencies:")
    print("  Source Tables:", dependencies["source_tables"])
    print("  Target Tables:", dependencies["target_tables"])
    print("  Columns:", dependencies["columns"])