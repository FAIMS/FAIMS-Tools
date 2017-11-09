package formatter;

import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class StatementParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.4", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__17=1, T__16=2, T__15=3, T__14=4, T__13=5, T__12=6, T__11=7, T__10=8, 
		T__9=9, T__8=10, T__7=11, T__6=12, T__5=13, T__4=14, T__3=15, T__2=16, 
		T__1=17, T__0=18, NEWLINE=19, SPACE=20, STRING=21, NUMBER=22, INT=23, 
		VARIABLE=24;
	public static final String[] tokenNames = {
		"<INVALID>", "'or('", "'not('", "']'", "'greaterThanEqual('", "')'", "'elsif'", 
		"','", "'between('", "'['", "'if'", "'and('", "'lessThan('", "'lessThanEqual('", 
		"'equal('", "'then'", "'greaterThan('", "'else'", "'in('", "'\n'", "SPACE", 
		"STRING", "NUMBER", "INT", "VARIABLE"
	};
	public static final int
		RULE_program = 0, RULE_statement = 1, RULE_next_statement = 2, RULE_multi_expression = 3, 
		RULE_single_expression = 4, RULE_list = 5, RULE_literals = 6, RULE_literal = 7;
	public static final String[] ruleNames = {
		"program", "statement", "next_statement", "multi_expression", "single_expression", 
		"list", "literals", "literal"
	};

	@Override
	public String getGrammarFileName() { return "Statement.g4"; }

	@Override
	public String[] getTokenNames() { return tokenNames; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public StatementParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class ProgramContext extends ParserRuleContext {
		public String value;
		public StatementContext s;
		public StatementContext statement() {
			return getRuleContext(StatementContext.class,0);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).enterProgram(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).exitProgram(this);
		}
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(16); ((ProgramContext)_localctx).s = statement();
			 
			            ((ProgramContext)_localctx).value =  ((ProgramContext)_localctx).s.value; 
			        
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class StatementContext extends ParserRuleContext {
		public String value;
		public Multi_expressionContext e;
		public LiteralContext v;
		public Next_statementContext s;
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public Multi_expressionContext multi_expression() {
			return getRuleContext(Multi_expressionContext.class,0);
		}
		public Next_statementContext next_statement() {
			return getRuleContext(Next_statementContext.class,0);
		}
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).enterStatement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).exitStatement(this);
		}
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_statement);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(19); match(T__8);
			setState(20); ((StatementContext)_localctx).e = multi_expression();
			setState(21); match(T__3);
			setState(22); ((StatementContext)_localctx).v = literal();
			setState(24);
			_la = _input.LA(1);
			if (_la==T__12 || _la==T__1) {
				{
				setState(23); ((StatementContext)_localctx).s = next_statement();
				}
			}

			 
			            if (((StatementContext)_localctx).e.value != null && ((StatementContext)_localctx).e.value == true)
			                ((StatementContext)_localctx).value =  ((StatementContext)_localctx).v.value;
			            else if (((StatementContext)_localctx).s != null)
			                ((StatementContext)_localctx).value =  ((StatementContext)_localctx).s.value;
			            else
			                ((StatementContext)_localctx).value =  "";
			        
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Next_statementContext extends ParserRuleContext {
		public String value;
		public Multi_expressionContext e;
		public LiteralContext v;
		public Next_statementContext s;
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public Multi_expressionContext multi_expression() {
			return getRuleContext(Multi_expressionContext.class,0);
		}
		public Next_statementContext next_statement() {
			return getRuleContext(Next_statementContext.class,0);
		}
		public Next_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_next_statement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).enterNext_statement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).exitNext_statement(this);
		}
	}

	public final Next_statementContext next_statement() throws RecognitionException {
		Next_statementContext _localctx = new Next_statementContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_next_statement);
		int _la;
		try {
			setState(41);
			switch (_input.LA(1)) {
			case T__12:
				enterOuterAlt(_localctx, 1);
				{
				setState(28); match(T__12);
				setState(29); ((Next_statementContext)_localctx).e = multi_expression();
				setState(30); match(T__3);
				setState(31); ((Next_statementContext)_localctx).v = literal();
				setState(33);
				_la = _input.LA(1);
				if (_la==T__12 || _la==T__1) {
					{
					setState(32); ((Next_statementContext)_localctx).s = next_statement();
					}
				}

				 
				            if (((Next_statementContext)_localctx).e.value != null && ((Next_statementContext)_localctx).e.value == true)
				                ((Next_statementContext)_localctx).value =  ((Next_statementContext)_localctx).v.value;
				            else if (((Next_statementContext)_localctx).s != null)
				                ((Next_statementContext)_localctx).value =  ((Next_statementContext)_localctx).s.value;
				            else
				                ((Next_statementContext)_localctx).value =  "";
				        
				}
				break;
			case T__1:
				enterOuterAlt(_localctx, 2);
				{
				setState(37); match(T__1);
				setState(38); ((Next_statementContext)_localctx).v = literal();
				 
				            ((Next_statementContext)_localctx).value =  ((Next_statementContext)_localctx).v.value;
				        
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Multi_expressionContext extends ParserRuleContext {
		public Boolean value;
		public Single_expressionContext l;
		public Multi_expressionContext r;
		public Single_expressionContext e;
		public Multi_expressionContext multi_expression() {
			return getRuleContext(Multi_expressionContext.class,0);
		}
		public Single_expressionContext single_expression() {
			return getRuleContext(Single_expressionContext.class,0);
		}
		public Multi_expressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_multi_expression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).enterMulti_expression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).exitMulti_expression(this);
		}
	}

	public final Multi_expressionContext multi_expression() throws RecognitionException {
		Multi_expressionContext _localctx = new Multi_expressionContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_multi_expression);
		try {
			setState(60);
			switch (_input.LA(1)) {
			case T__7:
				enterOuterAlt(_localctx, 1);
				{
				setState(43); match(T__7);
				setState(44); ((Multi_expressionContext)_localctx).l = single_expression();
				setState(45); match(T__11);
				setState(46); ((Multi_expressionContext)_localctx).r = multi_expression();
				setState(47); match(T__13);
				 
				            ((Multi_expressionContext)_localctx).value =  (((Multi_expressionContext)_localctx).l.value != null && ((Multi_expressionContext)_localctx).l.value) && (((Multi_expressionContext)_localctx).r.value != null && ((Multi_expressionContext)_localctx).r.value); 
				        
				}
				break;
			case T__17:
				enterOuterAlt(_localctx, 2);
				{
				setState(50); match(T__17);
				setState(51); ((Multi_expressionContext)_localctx).l = single_expression();
				setState(52); match(T__11);
				setState(53); ((Multi_expressionContext)_localctx).r = multi_expression();
				setState(54); match(T__13);
				 
				            ((Multi_expressionContext)_localctx).value =  (((Multi_expressionContext)_localctx).l.value != null && ((Multi_expressionContext)_localctx).l.value) || (((Multi_expressionContext)_localctx).r.value != null && ((Multi_expressionContext)_localctx).r.value); 
				        
				}
				break;
			case T__16:
			case T__14:
			case T__10:
			case T__6:
			case T__5:
			case T__4:
			case T__2:
			case T__0:
			case STRING:
			case NUMBER:
			case INT:
			case VARIABLE:
				enterOuterAlt(_localctx, 3);
				{
				setState(57); ((Multi_expressionContext)_localctx).e = single_expression();
				 ((Multi_expressionContext)_localctx).value =  ((Multi_expressionContext)_localctx).e.value; 
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Single_expressionContext extends ParserRuleContext {
		public Boolean value;
		public LiteralContext l;
		public LiteralContext r;
		public LiteralContext min;
		public LiteralContext max;
		public Single_expressionContext e;
		public ListContext items;
		public ListContext list() {
			return getRuleContext(ListContext.class,0);
		}
		public List<LiteralContext> literal() {
			return getRuleContexts(LiteralContext.class);
		}
		public Single_expressionContext single_expression() {
			return getRuleContext(Single_expressionContext.class,0);
		}
		public LiteralContext literal(int i) {
			return getRuleContext(LiteralContext.class,i);
		}
		public Single_expressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_single_expression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).enterSingle_expression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).exitSingle_expression(this);
		}
	}

	public final Single_expressionContext single_expression() throws RecognitionException {
		Single_expressionContext _localctx = new Single_expressionContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_single_expression);
		try {
			setState(121);
			switch (_input.LA(1)) {
			case T__4:
				enterOuterAlt(_localctx, 1);
				{
				setState(62); match(T__4);
				setState(63); ((Single_expressionContext)_localctx).l = literal();
				setState(64); match(T__11);
				setState(65); ((Single_expressionContext)_localctx).r = literal();
				setState(66); match(T__13);

				            ((Single_expressionContext)_localctx).value =  (((Single_expressionContext)_localctx).l.value == null && ((Single_expressionContext)_localctx).r.value == null) || (((Single_expressionContext)_localctx).l.value != null && ((Single_expressionContext)_localctx).l.value.equals(((Single_expressionContext)_localctx).r.value));
				        
				}
				break;
			case T__2:
				enterOuterAlt(_localctx, 2);
				{
				setState(69); match(T__2);
				setState(70); ((Single_expressionContext)_localctx).l = literal();
				setState(71); match(T__11);
				setState(72); ((Single_expressionContext)_localctx).r = literal();
				setState(73); match(T__13);

				            ((Single_expressionContext)_localctx).value =  ((Single_expressionContext)_localctx).l.value != null && ((Single_expressionContext)_localctx).r.value != null && Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).l.value)) > Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).r.value));
				        
				}
				break;
			case T__14:
				enterOuterAlt(_localctx, 3);
				{
				setState(76); match(T__14);
				setState(77); ((Single_expressionContext)_localctx).l = literal();
				setState(78); match(T__11);
				setState(79); ((Single_expressionContext)_localctx).r = literal();
				setState(80); match(T__13);

				            ((Single_expressionContext)_localctx).value =  ((Single_expressionContext)_localctx).l.value != null && ((Single_expressionContext)_localctx).r.value != null && Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).l.value)) >= Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).r.value));
				        
				}
				break;
			case T__6:
				enterOuterAlt(_localctx, 4);
				{
				setState(83); match(T__6);
				setState(84); ((Single_expressionContext)_localctx).l = literal();
				setState(85); match(T__11);
				setState(86); ((Single_expressionContext)_localctx).r = literal();
				setState(87); match(T__13);

				            ((Single_expressionContext)_localctx).value =  ((Single_expressionContext)_localctx).l.value != null && ((Single_expressionContext)_localctx).r.value != null && Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).l.value)) < Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).r.value));
				        
				}
				break;
			case T__5:
				enterOuterAlt(_localctx, 5);
				{
				setState(90); match(T__5);
				setState(91); ((Single_expressionContext)_localctx).l = literal();
				setState(92); match(T__11);
				setState(93); ((Single_expressionContext)_localctx).r = literal();
				setState(94); match(T__13);

				            ((Single_expressionContext)_localctx).value =  ((Single_expressionContext)_localctx).l.value != null && ((Single_expressionContext)_localctx).r.value != null && Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).l.value)) <= Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).r.value));
				        
				}
				break;
			case T__10:
				enterOuterAlt(_localctx, 6);
				{
				setState(97); match(T__10);
				setState(98); ((Single_expressionContext)_localctx).l = literal();
				setState(99); match(T__11);
				setState(100); ((Single_expressionContext)_localctx).min = literal();
				setState(101); match(T__11);
				setState(102); ((Single_expressionContext)_localctx).max = literal();
				setState(103); match(T__13);

				            ((Single_expressionContext)_localctx).value =  ((Single_expressionContext)_localctx).l.value != null && ((Single_expressionContext)_localctx).min.value != null && ((Single_expressionContext)_localctx).max.value != null && Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).l.value)) >= Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).min.value)) && Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).l.value)) <= Float.parseFloat(String.valueOf(((Single_expressionContext)_localctx).max.value));
				        
				}
				break;
			case T__16:
				enterOuterAlt(_localctx, 7);
				{
				setState(106); match(T__16);
				setState(107); ((Single_expressionContext)_localctx).e = single_expression();
				setState(108); match(T__13);
				 
				            if (((Single_expressionContext)_localctx).e.value != null && ((Single_expressionContext)_localctx).e.value == true)
				                ((Single_expressionContext)_localctx).value =  false;
				            else
				                ((Single_expressionContext)_localctx).value =  true;
				        
				}
				break;
			case T__0:
				enterOuterAlt(_localctx, 8);
				{
				setState(111); match(T__0);
				setState(112); ((Single_expressionContext)_localctx).l = literal();
				setState(113); match(T__11);
				setState(114); ((Single_expressionContext)_localctx).items = list();
				setState(115); match(T__13);
				 ((Single_expressionContext)_localctx).value =  ((Single_expressionContext)_localctx).items.value != null && ((Single_expressionContext)_localctx).items.value.indexOf(((Single_expressionContext)_localctx).l.value) >= 0; 
				}
				break;
			case STRING:
			case NUMBER:
			case INT:
			case VARIABLE:
				enterOuterAlt(_localctx, 9);
				{
				setState(118); ((Single_expressionContext)_localctx).l = literal();
				 ((Single_expressionContext)_localctx).value =  ((Single_expressionContext)_localctx).l.value != null; 
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ListContext extends ParserRuleContext {
		public java.util.ArrayList value;
		public LiteralsContext l;
		public LiteralsContext literals() {
			return getRuleContext(LiteralsContext.class,0);
		}
		public ListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_list; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).enterList(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).exitList(this);
		}
	}

	public final ListContext list() throws RecognitionException {
		ListContext _localctx = new ListContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_list);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(123); match(T__9);
			setState(124); ((ListContext)_localctx).l = literals();
			setState(125); match(T__15);
			 ((ListContext)_localctx).value =  ((ListContext)_localctx).l.value; 
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LiteralsContext extends ParserRuleContext {
		public java.util.ArrayList value;
		public LiteralContext l;
		public LiteralsContext rest;
		public LiteralsContext literals() {
			return getRuleContext(LiteralsContext.class,0);
		}
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public LiteralsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literals; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).enterLiterals(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).exitLiterals(this);
		}
	}

	public final LiteralsContext literals() throws RecognitionException {
		LiteralsContext _localctx = new LiteralsContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_literals);
		try {
			setState(136);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(128); ((LiteralsContext)_localctx).l = literal();
				setState(129); match(T__11);
				setState(130); ((LiteralsContext)_localctx).rest = literals();

				            ((LiteralsContext)_localctx).value =  ((LiteralsContext)_localctx).rest.value;
				            _localctx.value.add(((LiteralsContext)_localctx).l.value);
				        
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(133); ((LiteralsContext)_localctx).l = literal();

				            ((LiteralsContext)_localctx).value =  new java.util.ArrayList();
				            _localctx.value.add(((LiteralsContext)_localctx).l.value);
				        
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LiteralContext extends ParserRuleContext {
		public String value;
		public Token s;
		public Token v;
		public Token n;
		public Token i;
		public TerminalNode INT() { return getToken(StatementParser.INT, 0); }
		public TerminalNode VARIABLE() { return getToken(StatementParser.VARIABLE, 0); }
		public TerminalNode NUMBER() { return getToken(StatementParser.NUMBER, 0); }
		public TerminalNode STRING() { return getToken(StatementParser.STRING, 0); }
		public LiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literal; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).enterLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof StatementListener ) ((StatementListener)listener).exitLiteral(this);
		}
	}

	public final LiteralContext literal() throws RecognitionException {
		LiteralContext _localctx = new LiteralContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_literal);
		try {
			setState(146);
			switch (_input.LA(1)) {
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(138); ((LiteralContext)_localctx).s = match(STRING);

				            if ((((LiteralContext)_localctx).s!=null?((LiteralContext)_localctx).s.getText():null) != null) {
				                ((LiteralContext)_localctx).value =  (((LiteralContext)_localctx).s!=null?((LiteralContext)_localctx).s.getText():null).substring(1,(((LiteralContext)_localctx).s!=null?((LiteralContext)_localctx).s.getText():null).length()-1);
				            }
				        
				}
				break;
			case VARIABLE:
				enterOuterAlt(_localctx, 2);
				{
				setState(140); ((LiteralContext)_localctx).v = match(VARIABLE);

				            if ((((LiteralContext)_localctx).v!=null?((LiteralContext)_localctx).v.getText():null) != null) {
				                ((LiteralContext)_localctx).value =  ArgumentMap.getValue((((LiteralContext)_localctx).v!=null?((LiteralContext)_localctx).v.getText():null));
				            }
				        
				}
				break;
			case NUMBER:
				enterOuterAlt(_localctx, 3);
				{
				setState(142); ((LiteralContext)_localctx).n = match(NUMBER);

				            if ((((LiteralContext)_localctx).n!=null?((LiteralContext)_localctx).n.getText():null) != null) {
				                ((LiteralContext)_localctx).value =  (((LiteralContext)_localctx).n!=null?((LiteralContext)_localctx).n.getText():null);
				            }
				        
				}
				break;
			case INT:
				enterOuterAlt(_localctx, 4);
				{
				setState(144); ((LiteralContext)_localctx).i = match(INT);

				            if ((((LiteralContext)_localctx).i!=null?((LiteralContext)_localctx).i.getText():null) != null) {
				                ((LiteralContext)_localctx).value =  (((LiteralContext)_localctx).i!=null?((LiteralContext)_localctx).i.getText():null);
				            }
				        
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\32\u0097\4\2\t\2"+
		"\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\3\2\3\2\3\2\3"+
		"\3\3\3\3\3\3\3\3\3\5\3\33\n\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\5\4$\n\4\3\4"+
		"\3\4\3\4\3\4\3\4\3\4\5\4,\n\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5"+
		"\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5?\n\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6"+
		"\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3"+
		"\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6"+
		"\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6|"+
		"\n\6\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\b\u008b\n\b"+
		"\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\5\t\u0095\n\t\3\t\2\2\n\2\4\6\b\n\f\16"+
		"\20\2\2\u009f\2\22\3\2\2\2\4\25\3\2\2\2\6+\3\2\2\2\b>\3\2\2\2\n{\3\2\2"+
		"\2\f}\3\2\2\2\16\u008a\3\2\2\2\20\u0094\3\2\2\2\22\23\5\4\3\2\23\24\b"+
		"\2\1\2\24\3\3\2\2\2\25\26\7\f\2\2\26\27\5\b\5\2\27\30\7\21\2\2\30\32\5"+
		"\20\t\2\31\33\5\6\4\2\32\31\3\2\2\2\32\33\3\2\2\2\33\34\3\2\2\2\34\35"+
		"\b\3\1\2\35\5\3\2\2\2\36\37\7\b\2\2\37 \5\b\5\2 !\7\21\2\2!#\5\20\t\2"+
		"\"$\5\6\4\2#\"\3\2\2\2#$\3\2\2\2$%\3\2\2\2%&\b\4\1\2&,\3\2\2\2\'(\7\23"+
		"\2\2()\5\20\t\2)*\b\4\1\2*,\3\2\2\2+\36\3\2\2\2+\'\3\2\2\2,\7\3\2\2\2"+
		"-.\7\r\2\2./\5\n\6\2/\60\7\t\2\2\60\61\5\b\5\2\61\62\7\7\2\2\62\63\b\5"+
		"\1\2\63?\3\2\2\2\64\65\7\3\2\2\65\66\5\n\6\2\66\67\7\t\2\2\678\5\b\5\2"+
		"89\7\7\2\29:\b\5\1\2:?\3\2\2\2;<\5\n\6\2<=\b\5\1\2=?\3\2\2\2>-\3\2\2\2"+
		">\64\3\2\2\2>;\3\2\2\2?\t\3\2\2\2@A\7\20\2\2AB\5\20\t\2BC\7\t\2\2CD\5"+
		"\20\t\2DE\7\7\2\2EF\b\6\1\2F|\3\2\2\2GH\7\22\2\2HI\5\20\t\2IJ\7\t\2\2"+
		"JK\5\20\t\2KL\7\7\2\2LM\b\6\1\2M|\3\2\2\2NO\7\6\2\2OP\5\20\t\2PQ\7\t\2"+
		"\2QR\5\20\t\2RS\7\7\2\2ST\b\6\1\2T|\3\2\2\2UV\7\16\2\2VW\5\20\t\2WX\7"+
		"\t\2\2XY\5\20\t\2YZ\7\7\2\2Z[\b\6\1\2[|\3\2\2\2\\]\7\17\2\2]^\5\20\t\2"+
		"^_\7\t\2\2_`\5\20\t\2`a\7\7\2\2ab\b\6\1\2b|\3\2\2\2cd\7\n\2\2de\5\20\t"+
		"\2ef\7\t\2\2fg\5\20\t\2gh\7\t\2\2hi\5\20\t\2ij\7\7\2\2jk\b\6\1\2k|\3\2"+
		"\2\2lm\7\4\2\2mn\5\n\6\2no\7\7\2\2op\b\6\1\2p|\3\2\2\2qr\7\24\2\2rs\5"+
		"\20\t\2st\7\t\2\2tu\5\f\7\2uv\7\7\2\2vw\b\6\1\2w|\3\2\2\2xy\5\20\t\2y"+
		"z\b\6\1\2z|\3\2\2\2{@\3\2\2\2{G\3\2\2\2{N\3\2\2\2{U\3\2\2\2{\\\3\2\2\2"+
		"{c\3\2\2\2{l\3\2\2\2{q\3\2\2\2{x\3\2\2\2|\13\3\2\2\2}~\7\13\2\2~\177\5"+
		"\16\b\2\177\u0080\7\5\2\2\u0080\u0081\b\7\1\2\u0081\r\3\2\2\2\u0082\u0083"+
		"\5\20\t\2\u0083\u0084\7\t\2\2\u0084\u0085\5\16\b\2\u0085\u0086\b\b\1\2"+
		"\u0086\u008b\3\2\2\2\u0087\u0088\5\20\t\2\u0088\u0089\b\b\1\2\u0089\u008b"+
		"\3\2\2\2\u008a\u0082\3\2\2\2\u008a\u0087\3\2\2\2\u008b\17\3\2\2\2\u008c"+
		"\u008d\7\27\2\2\u008d\u0095\b\t\1\2\u008e\u008f\7\32\2\2\u008f\u0095\b"+
		"\t\1\2\u0090\u0091\7\30\2\2\u0091\u0095\b\t\1\2\u0092\u0093\7\31\2\2\u0093"+
		"\u0095\b\t\1\2\u0094\u008c\3\2\2\2\u0094\u008e\3\2\2\2\u0094\u0090\3\2"+
		"\2\2\u0094\u0092\3\2\2\2\u0095\21\3\2\2\2\t\32#+>{\u008a\u0094";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}
