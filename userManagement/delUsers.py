import mechanize, re, sys


br = mechanize.Browser()
br.open("http://localhost")

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)


br.form = list(br.forms())[0]

br.form['user[email]']="faimsadmin@intersect.org.au"
br.form['user[password]']="Pass.123"

br.submit()

todo=[]

delTodo=[]

for link in br.links():
	moduleMatch = re.compile("/project_modules/[0-9]+").search(link.url)
	if moduleMatch:
		todo.append(link)

for link in todo:
#	print link
	br.follow_link(link)
	br.follow_link(br.find_link(url_regex=re.compile(".*edit_project_module_user")))

	#br.form = list(br.forms())[0]

	for l in br.links():		
		#print l.url
	        moduleMatch = re.compile("(remove_project_module_user/[2-9]$)|(remove_project_module_user/[1-9][0-9])").search(l.url)
		if moduleMatch:
			print "Match"
			print l.url
			br.form = list(br.forms())[0]
			br.form.action = "http://localhost"+l.url
			br.submit()
		
