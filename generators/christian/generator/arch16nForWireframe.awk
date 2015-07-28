BEGIN {print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>";
		print "<arch16ns>";
		FS="="}
// {print "<arch16n k=\"{"$1"}\"><![CDATA["$2"]]></arch16n>"}
END {print "</arch16ns>"}