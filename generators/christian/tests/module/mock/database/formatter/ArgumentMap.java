package formatter;

import java.util.concurrent.Semaphore;

public class ArgumentMap {

	private static Semaphore lock = new Semaphore(1);
    private static String[] globalArguments;

	public static String getValue(String argument) {
		String[] arguments = globalArguments;
		if (arguments == null) return null;
		int index = Integer.parseInt(argument.substring(1)) - 1;
		if (index < 0 || index >= arguments.length) return null;
		return arguments[index];
    }

	public static String apply(StringFormatter stringFormatter, String value) {
		if (value == null) return "";
		
		String[] arguments = globalArguments;
	    if (arguments == null) return value;
	    for (int i = 0; i < arguments.length; i++) {
	    	String argument = arguments[i];
	    	value = value.replaceAll("\\$" + (i + 1), argument == null ? "" : argument);
	    }
		return value;
	}
	
	public static synchronized void setArguments(StringFormatter stringFormatter, String[] arguments) throws Exception {
		lock.acquire();
		globalArguments = arguments;
	}

	public static synchronized void removeArguments(StringFormatter stringFormatter) {
		globalArguments = null;
		lock.release();
	}

}
