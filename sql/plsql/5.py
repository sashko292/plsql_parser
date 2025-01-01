import json
from antlr4 import FileStream, CommonTokenStream
from antlr4.tree.Tree import TerminalNode
from Python3.PlSqlLexer import PlSqlLexer
from Python3.PlSqlParser import PlSqlParser
from Python3.PlSqlParserVisitor import PlSqlParserVisitor


class DependencyVisitor(PlSqlParserVisitor):
    def __init__(self):
        super().__init__()
        self.table_dependencies = {}

    def visitCreate_table(self, ctx):
        """
        Process CREATE TABLE statements to extract target table and source tables.
        """
        try:
            created_table = ctx.table_name().getText()
            print(f"Found CREATE TABLE: {created_table}")
            source_tables = self._extract_sources(ctx)
            self.table_dependencies[created_table] = source_tables if source_tables else set()
        except Exception as e:
            print(f"Error processing CREATE TABLE: {e}")
        return super().visitCreate_table(ctx)

    def _extract_sources(self, node):
        """
        Recursively extract source tables from the parse tree node.
        """
        source_tables = set()
        if not hasattr(node, 'children') or not node.children:
            return source_tables

        for child in node.children:
            if isinstance(child, PlSqlParser.From_clauseContext):
                source_tables.update(self._parse_from_clause(child))
            elif isinstance(child, PlSqlParser.SubqueryContext):
                source_tables.update(self._extract_sources(child))
            elif isinstance(child, PlSqlParser.Tableview_nameContext):
                table_name = child.getText()
                print(f"Found source table: {table_name}")
                source_tables.add(table_name)
            elif isinstance(child, TerminalNode):  # Check for TerminalNode instead of TerminalNodeImpl
                print(f"Terminal node text: {child.getText()}")
            elif hasattr(child, "children"):
                source_tables.update(self._extract_sources(child))
            else:
                print(f"Skipping unhandled node of type: {type(child).__name__}")
        return source_tables

    def _parse_from_clause(self, from_clause):
        """
        Extract tables from FROM clause.
        """
        source_tables = set()
        try:
            table_refs = from_clause.table_ref_list().table_ref()
            if not table_refs:
                print("No table references found in FROM clause.")
                return source_tables

            for table_ref in table_refs:
                table_ref_aux = table_ref.table_ref_aux()
                if not table_ref_aux:
                    continue

                table_ref_internal = table_ref_aux.table_ref_aux_internal()
                if not table_ref_internal:
                    continue

                dml_table_clause = table_ref_internal.dml_table_expression_clause()
                if not dml_table_clause:
                    continue

                table_name_ctx = dml_table_clause.tableview_name()
                if table_name_ctx:
                    table_name = table_name_ctx.getText()
                    print(f"Found source table: {table_name}")
                    source_tables.add(table_name)
        except AttributeError as e:
            print(f"Error processing FROM clause: {e}")
        return source_tables


def parse_sql_file(sql_file_path):
    """
    Parse the SQL file and extract dependencies.
    """
    try:
        # Load and tokenize the SQL file
        input_stream = FileStream(sql_file_path, encoding="utf-8")
        lexer = PlSqlLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = PlSqlParser(token_stream)

        # Parse the SQL script
        print("Parsing SQL file...")
        tree = parser.sql_script()

        # Visit the parse tree to extract dependencies
        visitor = DependencyVisitor()
        visitor.visit(tree)

        # Print simplified table dependencies
        print("\nSimplified Table Dependencies:")
        for target, sources in visitor.table_dependencies.items():
            print(f"{target}: {', '.join(sources) if sources else 'No source tables found'}")

    except Exception as e:
        print(f"Error parsing SQL file: {e}")


if __name__ == "__main__":
    # Path to the SQL file
    sql_file_path = "load_data.sql"  # Update this to the actual path of your SQL file
    parse_sql_file(sql_file_path)