package formatter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;

public class StringFormatter {
	
	public static HashMap<String, CommonTokenStream> tokensMap;
	public static HashMap<String, List<Expression>> expressionsMap;
	
	class Expression {
		
		private String preMatch;
		private String statement;
		private int index;

		public Expression(String preMatch, String statement, int index) {
			this.preMatch = preMatch;
			this.statement = statement;
			this.index = index;
		}
		
		public String evaluate() throws Exception {
			String parsedStatement = statement;
			if (parsedStatement != null && !"".equals(parsedStatement.trim())) {
				StatementParser parser = new StatementParser(createOrFindLexer(parsedStatement));
				parsedStatement = parser.program().value;
			}
			String value = ArgumentMap.apply(StringFormatter.this, preMatch) + ArgumentMap.apply(StringFormatter.this, parsedStatement);
			return value;
		}
		
		private CommonTokenStream createOrFindLexer(String statement) {
			CommonTokenStream tokens;
			if (tokensMap.get(statement) != null) {
				tokens = tokensMap.get(statement);
			} else {
				StatementLexer lexer = new StatementLexer(new ANTLRInputStream(statement));
	            tokens = new CommonTokenStream(lexer);
	            tokens.fill();
	            
	            tokensMap.put(statement, tokens);
			}
			tokens.reset();
            return tokens;
		}
	}

	private String formatString;
	private List<Expression> expressions;
	
	public StringFormatter(String formatString) {
		this.formatString = formatString;

    if (tokensMap == null)
      tokensMap = new HashMap<String, CommonTokenStream>();
    if (expressionsMap == null)
      expressionsMap = new HashMap<String, List<Expression>>();
	}
	
	public StringFormatter preCompute() {
		createExpressions();
		return this;
	}
	
	public String evaluate(String[] arguments) throws Exception {
		String formattedValue = "";
		try {
			ArgumentMap.setArguments(this, arguments);		
			for (Expression expression : expressions) {
				formattedValue += expression.evaluate();
			}
		} finally {
			ArgumentMap.removeArguments(this);
		}
		return formattedValue;
	}
	
	private void createExpressions() {
		if (expressionsMap.get(formatString) != null) {
			expressions = expressionsMap.get(formatString);
		} else {
			expressions = new ArrayList<Expression>();
			
			int index = 0;
			int lastEnd = 0;
			String str = formatString;
			Pattern pattern = Pattern.compile("\\{\\{(([^\\}]||\\}(?!\\}))*)\\}\\}");
			Matcher matcher = pattern.matcher(str);
			while (true) {
				if (lastEnd < str.length() && matcher.find(lastEnd)) {
					index = matcher.start();
					String preMatch = "";
					if (matcher.start() > 0) {
						preMatch = str.substring(lastEnd, matcher.start());
					}
					String statement = str.substring(matcher.start() + 2, matcher.end() - 2);
					expressions.add(new Expression(preMatch, statement, index));
					lastEnd = matcher.end();
				} else {
					String preMatch = "";
					if (lastEnd < str.length()) {
						preMatch = str.substring(lastEnd);
					}
					expressions.add(new Expression(preMatch, null, index));
					break;
				}
			}
			
			expressionsMap.put(formatString, expressions);
		}
	}
	
	public static void init() {
		tokensMap = new HashMap<String, CommonTokenStream>();
		expressionsMap = new HashMap<String, List<Expression>>();
	}
}
