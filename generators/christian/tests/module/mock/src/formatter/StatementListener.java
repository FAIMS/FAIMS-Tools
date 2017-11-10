package formatter;

import org.antlr.v4.runtime.misc.NotNull;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link StatementParser}.
 */
public interface StatementListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link StatementParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(@NotNull StatementParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link StatementParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(@NotNull StatementParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link StatementParser#literals}.
	 * @param ctx the parse tree
	 */
	void enterLiterals(@NotNull StatementParser.LiteralsContext ctx);
	/**
	 * Exit a parse tree produced by {@link StatementParser#literals}.
	 * @param ctx the parse tree
	 */
	void exitLiterals(@NotNull StatementParser.LiteralsContext ctx);
	/**
	 * Enter a parse tree produced by {@link StatementParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(@NotNull StatementParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link StatementParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(@NotNull StatementParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link StatementParser#next_statement}.
	 * @param ctx the parse tree
	 */
	void enterNext_statement(@NotNull StatementParser.Next_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link StatementParser#next_statement}.
	 * @param ctx the parse tree
	 */
	void exitNext_statement(@NotNull StatementParser.Next_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link StatementParser#list}.
	 * @param ctx the parse tree
	 */
	void enterList(@NotNull StatementParser.ListContext ctx);
	/**
	 * Exit a parse tree produced by {@link StatementParser#list}.
	 * @param ctx the parse tree
	 */
	void exitList(@NotNull StatementParser.ListContext ctx);
	/**
	 * Enter a parse tree produced by {@link StatementParser#multi_expression}.
	 * @param ctx the parse tree
	 */
	void enterMulti_expression(@NotNull StatementParser.Multi_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link StatementParser#multi_expression}.
	 * @param ctx the parse tree
	 */
	void exitMulti_expression(@NotNull StatementParser.Multi_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link StatementParser#single_expression}.
	 * @param ctx the parse tree
	 */
	void enterSingle_expression(@NotNull StatementParser.Single_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link StatementParser#single_expression}.
	 * @param ctx the parse tree
	 */
	void exitSingle_expression(@NotNull StatementParser.Single_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link StatementParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(@NotNull StatementParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link StatementParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(@NotNull StatementParser.LiteralContext ctx);
}
