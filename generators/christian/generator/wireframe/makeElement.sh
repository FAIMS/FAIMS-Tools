#!/bin/bash
set -euo pipefail
tmp=$(mktemp -d)


#Takes as arguments: Name, Label, type, numColumns, HasAnnotation, HasCertainty, HasInfo, Required, ReadOnly, Path

#. - input        <input>
#. - dropdown     <select1>
#. - radio        <select1 appearance="full">
#. - button       <trigger>
#. - list         <select1 appearance="compact">
#. - checkbox     <select>
#  - map          <input faims_map="true">
#. - webview      <input faims_web="true">
#		square box
#. - pngicture      <select1 type="image">
# 		items with label
#  - camera       <select type="camera">
#		items with annotation/certainty
#  - file         <select type="file">
#		list with annotation


# required 	   Turns label red, TODO: write validation.xml, deploy validation tab, blankchecker logic
# noannotation Equivalent to faims_annotation="false"
# nocertainty  Equivalent to faims_certainty="false"
# noui         Only allows code to be generated for the data schema
# nodata       Only allows code to be generated for the UI schema
# readonly     Equivalent to faims_read_only="true"
# decimal

if [[ $# -ne 10 ]]; then
	echo "Takes as arguments: Name, Label, type, numColumns, HasAnnotation, HasCertainty, HasInfo, Required, ReadOnly, Path";
	exit 1;
fi		

width=`echo "(200/$4)" | bc`


echo $2 $3 $width


rm -f $tmp/drawfile.mvg
pwd=`pwd`
height=1;


case "$3" in
	input)
	if [ "$9" = "false" ]; then
		color="black"
	else
		color="gray"
	cat >> $tmp/drawfile.mvg <<- EOM
		<text x="7" y="30" font-family="Roboto" font-size="8" fill="gray"> Read only </text>
	EOM
	fi

	cat >> $tmp/drawfile.mvg <<- EOM

	<path d="M 5 30 L 5 35 L $[$width-5] 35 L $[$width-5] 30" stroke="$color" fill="white" stroke-width="1"/>
		
	EOM

	label=true
	normalFlags=true


	height=40


	;;

	dropdown)

	cat >> $tmp/drawfile.mvg <<- EOM

	<path d="M 5 35 L $[$width-5] 35" stroke="black" fill="black" stroke-width="1"/>
	<path d="M $[$width-15] 35 L $[$width-5] 35 L $[$width-5] 25 Z" stroke="black" fill="black" stroke-width="1"/>

	<text x="5" y="30" font-family="Roboto" font-size="8" fill="gray"> dropdown </text>

		line 5,75 $[$width-5],75 
		polyline $[$width-20],75 $[$width-5],75 $[$width-5],60

		fill gray
		stroke gray
		stroke-width 0
		stroke-opacity 0

		font-size 10
		text 10,70 "Dropdown"		
	EOM

	label=true
	normalFlags=true


	height=40

	;;

	radio)


	cat >> $tmp/drawfile.mvg <<- EOM
 		
 		<ellipse cx="7" cy="30" rx="5" ry="5"  style="fill:white;stroke:black;stroke-width:1" />
 		<ellipse cx="57" cy="30" rx="5" ry="5"  style="fill:white;stroke:black;stroke-width:1" />
 		<ellipse cx="107" cy="30" rx="5" ry="5"  style="fill:white;stroke:black;stroke-width:1" />
		<ellipse cx="157" cy="30" rx="5" ry="5"  style="fill:white;stroke:black;stroke-width:1" />

		<text x="15" y="32" font-family="Roboto" font-size="8" fill="gray"> Radio </text>
		<text x="65" y="32" font-family="Roboto" font-size="8" fill="gray"> Radio </text>
		<text x="115" y="32" font-family="Roboto" font-size="8" fill="gray"> Radio </text>
		<text x="165" y="32" font-family="Roboto" font-size="8" fill="gray"> Radio </text>

		fill white
		stroke gray

		circle 22,47 22,31
		circle 155,47 155,31
		circle 288,47 288,31

		fill gray
		stroke gray
		stroke-width 0
		stroke-opacity 0


		font-size 14
		text 43,52 "Radio"
		text 175,52 "Radio"
		text 318,52 "Radio"
		
	EOM

	label=true
	normalFlags=true


	height=40


	;;

	button)

	cat >> $tmp/drawfile.mvg <<- EOM

		<path d="M 5 5 L $[$width-5] 5 L $[$width-5] 35 L 5 35 Z" fill="lightgray"/>
		<text x="$[$width/2]" y="24" font-family="Roboto" font-size="9" fill="black" text-anchor="middle"> $2 </text>

		fill lightgray
		stroke lightgray

		polyline 5,5 $[$width-5],5 $[$width-5],75 5,75


		stroke-width 0
		stroke-opacity 0


		fill black
		stroke black
		stroke-width 0
		stroke-opacity 0


		font-size 20
		gravity center
		text 0,0 "$2"
		
	EOM

	label=false
	normalFlags=false


	height=40

	;;

	list)

	cat >> $tmp/drawfile.mvg <<- EOM
		<path d="M 15 35 L $[$width-15] 35 
		         M 15 55 L $[$width-15] 55 
		         M 15 75 L $[$width-15] 75
		         M 15 95 L $[$width-15] 95" stroke="gray" stroke-width="1"/>

		<text x="15" y="27" font-family="Roboto" font-size="8" fill="gray"> List </text>
		<text x="15" y="47" font-family="Roboto" font-size="8" fill="gray"> List </text>
		<text x="15" y="67" font-family="Roboto" font-size="8" fill="gray"> List </text>		
		<text x="15" y="87" font-family="Roboto" font-size="8" fill="gray"> List </text>			
		<text x="15" y="107" font-family="Roboto" font-size="8" fill="gray"> List </text>			

line 15,35 185,35
line 15,55 185,55
line 15,75 185,75
line 15,95 185,95


font-size 8
text 15,30 "List"
text 15,50 "List"
text 15,70 "List"
text 15,90 "List"
text 15,110 "List"


		
	EOM

	label=true
	normalFlags=false


	height=120
	;;

	checkbox)

	cat >> $tmp/drawfile.mvg <<- EOM

		fill white
		stroke gray

		<rect x="10" y="20" width="10" height="10" style="fill:white;stroke-width:1;stroke:black" />
		<rect x="10" y="40" width="10" height="10" style="fill:white;stroke-width:1;stroke:black" />
		<rect x="10" y="60" width="10" height="10" style="fill:white;stroke-width:1;stroke:black" />
		<rect x="10" y="80" width="10" height="10" style="fill:white;stroke-width:1;stroke:black" />

		<text x="25" y="28" font-family="Roboto" font-size="8" fill="gray"> Checkbox </text>
		<text x="25" y="48" font-family="Roboto" font-size="8" fill="gray"> Checkbox </text>
		<text x="25" y="68" font-family="Roboto" font-size="8" fill="gray"> Checkbox </text>
		<text x="25" y="88" font-family="Roboto" font-size="8" fill="gray"> Checkbox </text>



		polyline 10,40  10,55   25,55   25,40   10,40
		polyline 10,80  10,95   25,95   25,80   10,80
		polyline 10,120 10,135  25,135  25,120  10,120
		polyline 10,160 10,175  25,175  25,160  10,160

		fill gray
		stroke gray
		stroke-width 0
		stroke-opacity 0


		font-size 12
		text 35,53 "Checkbox"
		text 35,93 "Checkbox"
		text 35,133 "Checkbox"
		text 35,173 "Checkbox"



		
	EOM
	if [ "$5" = "true" ]; then
		#echo "<image width='20' height='20' x='$[$width-60]' y='4' xlink:href='$pwd/pencil.svg'/>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-30],20) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-30],40) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-30],60) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-30],80) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg


		#echo "image src-over $[$width-60],4 20,20 \"annotation.png\"" >> $tmp/drawfile.mvg
	fi

	if [ "$6" = "true" ]; then
		#echo "image src-over $[$width-40],4 20,20 \"certainty.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-15],20) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-15],40) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-15],60) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-15],80) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		
	fi
	if [ "$7" = "true" ]; then
		#echo "image src-over $[$width-20],4 20,20 \"info.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-15],0) scale(.6)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg
	fi




	label=true
	normalFlags=false


	height=100
	;;

	map)

	cat >> $tmp/drawfile.mvg <<- EOM

		<rect x="5" y="5" width="190" height="255" style="fill:gray;stroke-width:1;stroke:black"/>
		<text x="100" y="100" anchor="middle" font-family="Roboto" font-size="14" fill="black" text-anchor="middle"> Map Page </text>
		<rect x="5" y="265" width="61" height="30" style="fill:lightgray;stroke-width:0;stroke:black"/>
		<rect x="70" y="265" width="60" height="30" style="fill:lightgray;stroke-width:0;stroke:black"/>
		<rect x="134" y="265" width="61" height="30" style="fill:lightgray;stroke-width:0;stroke:black"/>

		<text x="35" y="284" anchor="middle" font-family="Roboto" font-size="10" fill="black" text-anchor="middle"> Centre Me </text>
		<text x="101" y="284" anchor="middle" font-family="Roboto" font-size="10" fill="black" text-anchor="middle"> Save Map Set </text>
		<text x="165" y="284" anchor="middle" font-family="Roboto" font-size="10" fill="black" text-anchor="middle"> User Defined </text>

		image src-over 0,0 400, 382 "mapSource.png"

		stroke lightgray
		fill lightgray

		polyline 5,387 133,387 133,407 5,407
		polyline 138,387 261,387 261,407 138,407
		polyline 266,387 395,387 395,407 266,407

		fill black

		font-size 12
		stroke-width 0
		stroke-opacity 0
		text 35,402 "Centre Me"

		text 160,402 "Save Map Set"

		text 290,402 "User Specified"

	EOM

	label=false
	normalFlags=false


	height=300

	;;

	webview)
	cat >> $tmp/drawfile.mvg <<- EOM
		<path d="M 5 5 L $[$width-5] 5 L $[$width-5] 75 L 5 75 Z" fill="#f0f0f0" stroke="black"/>
		<text x="$[$width/2]" y="46" font-family="Roboto" font-size="14" fill="black" text-anchor="middle"> $2 </text>

		fill lightblue
		stroke black
		stroke-width 0
		stroke-opacity 0


		polyline 5,5 5,155 $[$width-5],155 $[$width-5],5

		fill black

		gravity center

		font-size 24
		text 0,0 "$2"

	EOM
	height=80
	label=false
	normalFlags=false
	;;

	pictureGallery)
	cat >> $tmp/drawfile.mvg <<- EOM

		<rect x="5" y="35" width="40" height="42" style="fill:white;stroke-width:1;stroke:black"/>
		<rect x="55" y="35" width="40" height="42" style="fill:white;stroke-width:1;stroke:black"/>
		<rect x="105" y="35" width="40" height="42" style="fill:white;stroke-width:1;stroke:black"/>
		<rect x="155" y="35" width="40" height="42" style="fill:white;stroke-width:1;stroke:black"/>

		<text x="10" y="30"  font-family="Roboto" font-size="8" fill="black" > Picture 1 </text>
		<text x="60" y="30"  font-family="Roboto" font-size="8" fill="black" > Picture 2 </text>
		<text x="110" y="30"  font-family="Roboto" font-size="8" fill="black" > Picture 3 </text>
		<text x="160" y="30"  font-family="Roboto" font-size="8" fill="black" > Picture 4 </text>


	
	fill white

	stroke-width 2
	stroke-opacity 1

	polyline -40,55  75,55   75,160  -40,160
	polyline 85,55   190,55   190,160   85,160   85,55
	polyline 200,55  305,55  305,160  200,160  200,55
	polyline 315,55  460,55  460,160  315,160  315,55


	font-size 14
	fill black
	stroke-opacity 0

	text -25, 50 "Picture 1"
	text 110, 50 "Picture 2"
	text 225, 50 "Picture 3"
	text 340, 50 "Picture 4"



	EOM

	height=85
	label=true
	normalFlags=true
	;;

	camera)
	cat >> $tmp/drawfile.mvg <<- EOM

		<path d="M 5 30 L 95 30 L 95 80 L 5 80 Z" fill="white" stroke="black" stroke-width="1"/>
		<path d="M 105 30 L 195 30 L 195 80 L 105 80 Z" fill="white" stroke="black" stroke-width="1"/>

		<text x="15" y="27" font-family="Roboto" font-size="8pt" fill="black"> Camera 1 </text>
		<text x="115" y="27" font-family="Roboto" font-size="8pt" fill="black"> Camera 2 </text>


		font-size 14
		stroke-opacity 0
		text 50,39 "Camera 1"
		text 255, 39 "Camera 2"

		stroke-opacity 1

		fill white

		stroke-width 2
		stroke-opacity 1

		polyline 5,45 195,45 195,155 5,155 5,45
		polyline 205,45 395,45 395,155 205,155 205,45
	EOM

	if [ "$5" = "true" ]; then
		#echo "<image width='20' height='20' x='$[$width-60]' y='4' xlink:href='$pwd/pencil.svg'/>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(70,17) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(170, 17) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg

		#echo "image src-over $[$width-60],4 20,20 \"annotation.png\"" >> $tmp/drawfile.mvg
	fi

	if [ "$6" = "true" ]; then
		#echo "image src-over $[$width-40],4 20,20 \"certainty.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate(80,17) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(180, 17) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg		
	fi
	if [ "$7" = "true" ]; then
		#echo "image src-over $[$width-20],4 20,20 \"info.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-15],0) scale(.6)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg
	fi

	
	height=85
	label=true
	normalFlags=false

	;;

	file)

	cat >> $tmp/drawfile.mvg <<- EOM

		<path d="M 20 40 L $[$width-20] 40 M 20 60 L $[$width-20] 60 M 20 80 L $[$width-20] 80 M 20 100 $[$width-20] 100" fill="white" stroke="gray" stroke-width="1"/>
		<text x="25" y="35" font-family="Roboto" font-size="8pt" fill="gray"> File List </text>
		<text x="25" y="55" font-family="Roboto" font-size="8pt" fill="gray"> File List </text>
		<text x="25" y="75" font-family="Roboto" font-size="8pt" fill="gray"> File List </text>
		<text x="25" y="95" font-family="Roboto" font-size="8pt" fill="gray"> File List </text>
		<text x="25" y="115" font-family="Roboto" font-size="8pt" fill="gray"> File List </text>

		fill gray
		stroke gray
		stroke-width 0
		stroke-opacity 0

		line 20,80 $[$width-20],80
		line 20,120 $[$width-20],120
		line 20,160 $[$width-20],160
		line 20,200 $[$width-20],200


		font-size 12
		text 25, 65 "FileList"
		text 25,105 "FileList"
		text 25,145 "FileList"
		text 25,185 "FileList"
		text 25,225 "FileList"


		fill black
		stroke black
		stroke-width 0
		stroke-opacity 0

		
	EOM
	if [ "$5" = "true" ]; then
		#echo "<image width='20' height='20' x='$[$width-60]' y='4' xlink:href='$pwd/pencil.svg'/>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-50],25) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-50],45) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-50],65) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-50],85) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-50],105) scale(.4)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		#echo "image src-over $[$width-60],4 20,20 \"annotation.png\"" >> $tmp/drawfile.mvg
	fi

	if [ "$6" = "true" ]; then
		#echo "image src-over $[$width-40],4 20,20 \"certainty.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-40],25) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-40],45) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-40],65) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg		
		echo "<g transform='translate($[$width-40],85) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-40],105) scale(.4)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
	fi
	if [ "$7" = "true" ]; then
		#echo "image src-over $[$width-20],4 20,20 \"info.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-15],0) scale(.6)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg
	fi




	
	height=125
	label=true
	normalFlags=false

	;;

	latlong)

	cat >> $tmp/drawfile.mvg <<- EOM


	<text x="5" y="12" font-family="Roboto" font-size="10pt" fill="black"> Latitude </text>
	<text x="105" y="12" font-family="Roboto" font-size="10pt" fill="black"> Longitude </text>
	<text x="5" y="52" font-family="Roboto" font-size="10pt" fill="black"> Easting </text>
	<text x="105" y="52" font-family="Roboto" font-size="10pt" fill="black"> Northing </text>
	<text x="5" y="132" font-family="Roboto" font-size="10pt" fill="black"> Elevation (mASL) </text>



	<path d="M 5 30 L 5 35 L 95 35 L 95 30 M 105 30 L 105 35 L 195 35 L 195 30 M 5 70 L 5 75 L 95 75 L 95 70 M 105 70 L 105 75 L 195 75 L 195 70" stroke="black" fill="white" stroke-width="1"/>
	<rect x="5" y="85" width="190" height="30" style="fill:lightgray;stroke-width:0;stroke:black" />
	<text x="100" y="105" font-family="Roboto" font-size="10pt" fill="black" text-anchor="middle"> Take GPS Point </text>

	<path d="M 5 155 L 5 160 L 195 160 L 195 155" stroke="black" fill="white" stroke-width="1"/>

	EOM


	if [ "$5" = "true" ]; then
		#echo "<image width='20' height='20' x='$[$width-60]' y='4' xlink:href='$pwd/pencil.svg'/>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(64,0) scale(.5)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(164,0) scale(.5)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(64,40) scale(.5)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(164,40) scale(.5)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(164,120) scale(.5)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		#echo "image src-over $[$width-60],4 20,20 \"annotation.png\"" >> $tmp/drawfile.mvg
	fi

	if [ "$6" = "true" ]; then
		#echo "image src-over $[$width-40],4 20,20 \"certainty.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate(76,0) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(176,0) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(76,40) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(176,40) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(176,120) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg


	fi
	if [ "$7" = "true" ]; then
		#echo "image src-over $[$width-20],4 20,20 \"info.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate(88,0) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(188,0) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(88,40) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(188,40) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg
		echo "<g transform='translate(188,120) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg

	fi


	height=165
	label=false
	normalFlags=false
	;;

	*)
		echo "help! I don't know what to do with:" $3	

		cat - <<EOM
Valid arguments are:		
* input        <input>
* dropdown     <select1>
* radio        <select1 appearance="full">
* button       <trigger>
* list         <select1 appearance="compact">
* checkbox     <select>
* map          <input faims_map="true">
* webview      <input faims_web="true">
* pictureGallery      <select1 type="image">
* camera       <select type="camera">
* file         <select type="file">

EOM
		exit 1		
esac	


if [ $label = true ]; then
	if [ "$8" = "true" ]; then
		cat >> $tmp/drawfile.mvg <<- EOM
			<text x="5" y="12" font-family="Roboto" font-size="10pt" fill="red"> $2 </text>
			stroke red
			fill red
			stroke-width 0
			stroke-opacity 0
			font-size 16
	EOM
	else
		cat >> $tmp/drawfile.mvg <<- EOM
			<text x="5" y="12" font-family="Roboto" font-size="10pt" fill="black"> $2 </text>
			stroke black
			fill black
			stroke-width 0
			stroke-opacity 0
			font-size 16
	EOM
	fi



fi

if [ $normalFlags = true ]; then


	#echo $5 $6 $7
	if [ "$5" = "true" ]; then
		#echo "<image width='20' height='20' x='$[$width-60]' y='4' xlink:href='$pwd/pencil.svg'/>" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-36],0) scale(.5)'><path d='M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z' /></g>" >> $tmp/drawfile.mvg
		#echo "image src-over $[$width-60],4 20,20 \"annotation.png\"" >> $tmp/drawfile.mvg
	fi

	if [ "$6" = "true" ]; then
		#echo "image src-over $[$width-40],4 20,20 \"certainty.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-24],0) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M10,19H13V22H10V19M12,2A6,6 0 0,1 18,8C17.67,9.33 17.33,10.67 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C14.33,10 14.67,9 15,8A3,3 0 0,0 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z' /></g>" >> $tmp/drawfile.mvg
	fi
	if [ "$7" = "true" ]; then
		#echo "image src-over $[$width-20],4 20,20 \"info.png\"" >> $tmp/drawfile.mvg
		echo "<g transform='translate($[$width-12],0) scale(.5)'><path  width='20' height='20' x='$[$width-40]' y='4' d='M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z' /></g>" >> $tmp/drawfile.mvg
	fi
fi
cat > ${10}/$1.svg <<- EOM
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="$[$width]" height="$[$height]" 
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
     <style>
@font-face {
    font-family: 'Roboto';
    src: url('/usr/share/fonts/truetype/roboto/Roboto.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}

</style> 
<rect x="0" y="0" width="$[$width]" height="$[$height]" 
        fill="white" stroke-width="0"/>
EOM


#cat $tmp/drawfile.mvg
#convert  ${10}/$1.svg ${10}/$1.png


cat $tmp/drawfile.mvg >> ${10}/$1.svg

cat >> ${10}/$1.svg <<- EOM
</svg>
EOM

rm -rf $tmp

#cat ${10}/$1.svg
#convert ${10}/$1.svg ${10}/$1.png 
