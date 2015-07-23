import mechanize, re, sys


if (len(sys.argv) != 3):
	print "python addUser.py fname lname"
	sys.exit(1)
	

br = mechanize.Browser()
br.open("http://localhost")

br.form = list(br.forms())[0]

br.form['user[email]']="faimsadmin@intersect.org.au"
br.form['user[password]']="Pass.123"

br.submit()

todo=[]

for link in br.links():
	moduleMatch = re.compile("/project_modules/[0-9]+").search(link.url)
	if moduleMatch:
		todo.append(link)

for link in todo:
	#print link
	br.follow_link(link)
	br.follow_link(br.find_link(url_regex=re.compile(".*edit_project_module_user")))

	br.form = list(br.forms())[0]
	
	control=br.form.find_control("user_id")
	#print control.items
	for item in control.items:
		userMatch = re.compile(sys.argv[1]+" "+sys.argv[2]).search(str([label.text for label in item.get_labels()]))
		if userMatch:
			control.value = [item.name]
			print control.value		
			br.submit()
