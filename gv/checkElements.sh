#!/bin/bash
set -euo pipefail

#Takes as arguments: Name, Label, type, numColumns, HasAnnotation, HasCertainty, HasInfo

#. - button       <trigger>
#  - camera       <select type="camera">
#. - checkbox     <select>
#. - dropdown     <select1>
#  - file         <select type="file">
#. - input        <input>
#. - list         <select1 appearance="compact">
#  - map          <input faims_map="true">
#. - picture      <select1 type="image">
#. - radio        <select1 appearance="full">
#. - webview      <input faims_web="true">


# noannotation Equivalent to faims_annotation="false"
# nocertainty  Equivalent to faims_certainty="false"
# onlydata     Only allows code to be generated for the data schema
# onlyui       Only allows code to be generated for the UI schema
# readonly     Equivalent to faims_read_only="true"

rm -rf false testImages
mkdir false testImages

./makeElement.sh Required-Input1 "Input 1 Required" input 1 true true true true false testImages
./makeElement.sh Required-Input2 "Input 2 Required" input 1 false true true true false testImages
./makeElement.sh Required-Input3 "Input 3 Required" input 2 true false true true false testImages
./makeElement.sh Required-Input4 "Input 4 Required" input 2 false false true true false testImages
./makeElement.sh Required-Input5 "Input 5 Required" input 3 true false false true false testImages
./makeElement.sh Required-Input6 "Input 6 Required" input 3 false false false true false testImages
./makeElement.sh Required-Input7 "Input 7 Required" input 4 true false false true false testImages
./makeElement.sh Required-Input8 "Input 8 Required" input 4 false false false true false testImages

./makeElement.sh Input1 "Input 1 Label" input 4 true true true false false testImages
./makeElement.sh Input2 "Input 2 Label" input 4 false true true false false testImages
./makeElement.sh Input3 "Input 3 Label" input 3 true false true false false testImages
./makeElement.sh Input4 "Input 4 Label" input 3 false false true false false testImages
./makeElement.sh Input5 "Input 5 Label" input 2 true false false false false testImages
./makeElement.sh Input6 "Input 6 Label" input 2 false false false false false testImages
./makeElement.sh Input7 "Input 7 Label" input 1 true false false false false testImages
./makeElement.sh Input8 "Input 8 Label" input 1 false false false false false testImages

./makeElement.sh Readonly-Required-Input1 "readonly Input 1 Required" input 1 true true true true true testImages
./makeElement.sh Readonly-Required-Input2 "readonly Input 2 Required" input 1 false true true true true testImages
./makeElement.sh Readonly-Required-Input3 "readonly Input 3 Required" input 2 true false true true true testImages
./makeElement.sh Readonly-Required-Input4 "readonly Input 4 Required" input 2 false false true true true testImages
./makeElement.sh Readonly-Required-Input5 "readonly Input 5 Required" input 3 true false false true true testImages
./makeElement.sh Readonly-Required-Input6 "readonly Input 6 Required" input 3 false false false true true testImages
./makeElement.sh Readonly-Required-Input7 "readonly Input 7 Required" input 4 true false false true true testImages
./makeElement.sh Readonly-Required-Input8 "readonly Input 8 Required" input 4 false false false true true testImages
./makeElement.sh Readonly-Input1 "readonly Input 1 Label" input 4 true true true false true testImages
./makeElement.sh Readonly-Input2 "readonly Input 2 Label" input 4 false true true false true testImages
./makeElement.sh Readonly-Input3 "readonly Input 3 Label" input 3 true false true false true testImages
./makeElement.sh Readonly-Input4 "readonly Input 4 Label" input 3 false false true false true testImages
./makeElement.sh Readonly-Input5 "readonly Input 5 Label" input 2 true false false false true testImages
./makeElement.sh Readonly-Input6 "readonly Input 6 Label" input 2 false false false false true testImages
./makeElement.sh Readonly-Input7 "readonly Input 7 Label" input 1 true false false false true testImages
./makeElement.sh Readonly-Input8 "readonly Input 8 Label" input 1 false false false false true testImages

./makeElement.sh Required-dropdown1 "dropdown 1 Required" dropdown 1 true true true true false testImages
./makeElement.sh Required-dropdown2 "dropdown 2 Required" dropdown 1 false true true true false testImages
./makeElement.sh Required-dropdown3 "dropdown 3 Required" dropdown 2 true false true true false testImages
./makeElement.sh Required-dropdown4 "dropdown 4 Required" dropdown 2 false false true true false testImages
./makeElement.sh Required-dropdown5 "dropdown 5 Required" dropdown 3 true false false true false testImages
./makeElement.sh Required-dropdown6 "dropdown 6 Required" dropdown 3 false false false true false testImages
./makeElement.sh Required-dropdown7 "dropdown 7 Required" dropdown 4 true false false true false testImages
./makeElement.sh Required-dropdown8 "dropdown 8 Required" dropdown 4 false false false true false testImages

./makeElement.sh dropdown1 "dropdown 1 Label" dropdown 4 true true true false false testImages
./makeElement.sh dropdown2 "dropdown 2 Label" dropdown 4 false true true false false testImages
./makeElement.sh dropdown3 "dropdown 3 Label" dropdown 3 true false true false false testImages
./makeElement.sh dropdown4 "dropdown 4 Label" dropdown 3 false false true false false testImages
./makeElement.sh dropdown5 "dropdown 5 Label" dropdown 2 true false false false false testImages
./makeElement.sh dropdown6 "dropdown 6 Label" dropdown 2 false false false false false testImages
./makeElement.sh dropdown7 "dropdown 7 Label" dropdown 1 true false false false false testImages
./makeElement.sh dropdown8 "dropdown 8 Label" dropdown 1 false false false false false testImages


./makeElement.sh Required-radio1 "radio 1 Required" radio 1 true true true true false testImages
./makeElement.sh Required-radio2 "radio 2 Required" radio 1 false true true true false testImages
./makeElement.sh Required-radio3 "radio 3 Required" radio 2 true false true true false testImages
./makeElement.sh Required-radio4 "radio 4 Required" radio 2 false false true true false testImages
./makeElement.sh Required-radio5 "radio 5 Required" radio 3 true false false true false testImages
./makeElement.sh Required-radio6 "radio 6 Required" radio 3 false false false true false testImages
./makeElement.sh Required-radio7 "radio 7 Required" radio 4 true false false true false testImages
./makeElement.sh Required-radio8 "radio 8 Required" radio 4 false false false true false testImages

./makeElement.sh radio1 "radio 1 Label" radio 4 true true true false false testImages
./makeElement.sh radio2 "radio 2 Label" radio 4 false true true false false testImages
./makeElement.sh radio3 "radio 3 Label" radio 3 true false true false false testImages
./makeElement.sh radio4 "radio 4 Label" radio 3 false false true false false testImages
./makeElement.sh radio5 "radio 5 Label" radio 2 true false false false false testImages
./makeElement.sh radio6 "radio 6 Label" radio 2 false false false false false testImages
./makeElement.sh radio7 "radio 7 Label" radio 1 true false false false false testImages
./makeElement.sh radio8 "radio 8 Label" radio 1 false false false false false testImages

./makeElement.sh button1 "button 1 Label" button 4 true true true false false testImages
./makeElement.sh button3 "button 3 Label" button 3 true false true false false testImages
./makeElement.sh button5 "button 5 Label" button 2 true false false false false testImages
./makeElement.sh button7 "button 7 Label" button 1 true false false false false testImages

./makeElement.sh list1 "list 1 Label" list 4 true true true false false testImages
./makeElement.sh list3 "list 3 Label" list 3 true false true false false testImages
./makeElement.sh list5 "list 5 Label" list 2 true false false false false testImages
./makeElement.sh list7 "list 7 Label" list 1 true false false false false testImages

./makeElement.sh Required-checkbox1 "checkbox 1 Required" checkbox 1 true true true true false testImages
./makeElement.sh Required-checkbox2 "checkbox 2 Required" checkbox 1 false true true true false testImages
./makeElement.sh Required-checkbox3 "checkbox 3 Required" checkbox 2 true false true true false testImages
./makeElement.sh Required-checkbox4 "checkbox 4 Required" checkbox 2 false false true true false testImages
./makeElement.sh Required-checkbox5 "checkbox 5 Required" checkbox 3 true false false true false testImages
./makeElement.sh Required-checkbox6 "checkbox 6 Required" checkbox 3 false false false true false testImages
./makeElement.sh Required-checkbox7 "checkbox 7 Required" checkbox 4 true false false true false testImages
./makeElement.sh Required-checkbox8 "checkbox 8 Required" checkbox 4 false false false true false testImages

./makeElement.sh checkbox1 "checkbox 1 Label" checkbox 4 true true true false false testImages
./makeElement.sh checkbox2 "checkbox 2 Label" checkbox 4 false true true false false testImages
./makeElement.sh checkbox3 "checkbox 3 Label" checkbox 3 true false true false false testImages
./makeElement.sh checkbox4 "checkbox 4 Label" checkbox 3 false false true false false testImages
./makeElement.sh checkbox5 "checkbox 5 Label" checkbox 2 true false false false false testImages
./makeElement.sh checkbox6 "checkbox 6 Label" checkbox 2 false false false false false testImages
./makeElement.sh checkbox7 "checkbox 7 Label" checkbox 1 true false false false false testImages
./makeElement.sh checkbox8 "checkbox 8 Label" checkbox 1 false false false false false testImages

./makeElement.sh map1 "map" map 1 false false false false false testImages
./makeElement.sh map2 "map" map 1 false false false false false testImages
./makeElement.sh map3 "map" map 1 false false false false false testImages
./makeElement.sh map4 "map" map 1 false false false false false testImages


./makeElement.sh webview1 "webview 1" webview 1 false false false false false testImages
./makeElement.sh webview2 "webview 2" webview 2 false false false false false testImages
./makeElement.sh webview3 "webview 3" webview 3 false false false false false testImages
./makeElement.sh webview4 "webview 4" webview 4 false false false false false testImages

./makeElement.sh Required-pictureGallery1 "pictureGallery 1 Required" pictureGallery 1 true true true true false testImages
./makeElement.sh Required-pictureGallery2 "pictureGallery 2 Required" pictureGallery 1 false true true true false testImages
./makeElement.sh Required-pictureGallery3 "pictureGallery 3 Required" pictureGallery 1 true false true true false testImages
./makeElement.sh Required-pictureGallery4 "pictureGallery 4 Required" pictureGallery 1 false false true true false testImages
./makeElement.sh Required-pictureGallery5 "pictureGallery 5 Required" pictureGallery 1 true false false true false testImages
./makeElement.sh Required-pictureGallery6 "pictureGallery 6 Required" pictureGallery 1 false false false true false testImages
./makeElement.sh Required-pictureGallery7 "pictureGallery 7 Required" pictureGallery 1 true false false true false testImages
./makeElement.sh Required-pictureGallery8 "pictureGallery 8 Required" pictureGallery 1 false false false true false testImages

./makeElement.sh pictureGallery1 "pictureGallery 1 Label" pictureGallery 1 true true true false false testImages
./makeElement.sh pictureGallery2 "pictureGallery 2 Label" pictureGallery 1 false true true false false testImages
./makeElement.sh pictureGallery3 "pictureGallery 3 Label" pictureGallery 1 true false true false false testImages
./makeElement.sh pictureGallery4 "pictureGallery 4 Label" pictureGallery 1 false false true false false testImages
./makeElement.sh pictureGallery5 "pictureGallery 5 Label" pictureGallery 1 true false false false false testImages
./makeElement.sh pictureGallery6 "pictureGallery 6 Label" pictureGallery 1 false false false false false testImages
./makeElement.sh pictureGallery7 "pictureGallery 7 Label" pictureGallery 1 true false false false false testImages
./makeElement.sh pictureGallery8 "pictureGallery 8 Label" pictureGallery 1 false false false false false testImages

./makeElement.sh Required-camera1 "camera 1 Required" camera 1 true true true true false testImages
./makeElement.sh Required-camera2 "camera 2 Required" camera 1 false true true true false testImages
./makeElement.sh Required-camera3 "camera 3 Required" camera 1 true false true true false testImages
./makeElement.sh Required-camera4 "camera 4 Required" camera 1 false false true true false testImages
./makeElement.sh Required-camera5 "camera 5 Required" camera 1 true false false true false testImages
./makeElement.sh Required-camera6 "camera 6 Required" camera 1 false false false true false testImages
./makeElement.sh Required-camera7 "camera 7 Required" camera 1 true false false true false testImages
./makeElement.sh Required-camera8 "camera 8 Required" camera 1 false false false true false testImages

./makeElement.sh camera1 "camera 1 Label" camera 1 true true true false false testImages
./makeElement.sh camera2 "camera 2 Label" camera 1 false true true false false testImages
./makeElement.sh camera3 "camera 3 Label" camera 1 true false true false false testImages

./makeElement.sh camera4 "camera 4 Label" camera 1 false false true false false testImages
./makeElement.sh camera5 "camera 5 Label" camera 1 true false false false false testImages
./makeElement.sh camera6 "camera 6 Label" camera 1 false false false false false testImages
./makeElement.sh camera7 "camera 7 Label" camera 1 true false false false false testImages
./makeElement.sh camera8 "camera 8 Label" camera 1 false false false false false testImages

./makeElement.sh file1 "file 1 Label" file 1 true true true false false testImages
./makeElement.sh file2 "file 2 Label" file 1 false true true false false testImages
./makeElement.sh file3 "file 3 Label" file 1 true false true false false testImages
./makeElement.sh file4 "file 4 Label" file 1 false false true false false testImages
./makeElement.sh file5 "file 5 Label" file 1 true false false false false testImages
./makeElement.sh file6 "file 6 Label" file 1 false false false false false testImages
./makeElement.sh file7 "file 7 Label" file 1 true false false false false testImages
./makeElement.sh file8 "file 8 Label" file 1 false false false false false testImages


./makeElement.sh latlong1 "latlong 1 Label" latlong 1 true true true false false testImages
./makeElement.sh latlong2 "latlong 2 Label" latlong 1 false true true false false testImages
./makeElement.sh latlong3 "latlong 3 Label" latlong 1 true false true false false testImages
./makeElement.sh latlong4 "latlong 4 Label" latlong 1 false false true false false testImages
./makeElement.sh latlong5 "latlong 5 Label" latlong 1 true false false false false testImages
./makeElement.sh latlong6 "latlong 6 Label" latlong 1 false false false false false testImages
./makeElement.sh latlong7 "latlong 7 Label" latlong 1 true false false false false testImages
./makeElement.sh latlong8 "latlong 8 Label" latlong 1 false false false false false testImages


#montage false testImages/* -geometry +10+10 -border 2 -tile 4 -background lightgreen  allTestImages.pdf





./makeElement.sh userList "User List" list 1 true false false false false testImages
./makeElement.sh takeFeatureButton "Take a Feature" button 1 true false false false false testImages
./makeElement.sh startingBurialID "Starting Burial ID" input 1 false false false false false testImages
./makeElement.sh gpsDiagnostics "GPS Diagnostics" webview 1 false false false false false testImages
./makeElement.sh searchTerm "Search Term" input 2 false false false false false testImages
./makeElement.sh search "Search" button 2 true false false false false testImages
./makeElement.sh entityTypes "Entity Types" dropdown 2 false false false false false testImages
./makeElement.sh selectTrench "Select Trench" dropdown 2 false false false false false testImages
./makeElement.sh searchList "Search Results" list 1 true false false false false testImages

./makeElement.sh objectID "Object ID" input 1 false false true true false testImages
./makeElement.sh createdAt "Created At" input 1 false false false false false testImages
./makeElement.sh createdBy "Created By" input 1 false false false false false testImages
./makeElement.sh type "Type" dropdown 1 true true true false false testImages
./makeElement.sh siteSignificance "Site Significance" dropdown 1 true true true false false testImages
./makeElement.sh name "Name" input 1 true true true false false testImages
./makeElement.sh description "description" input 1 true true true false false testImages
./makeElement.sh source "Source" dropdown 1 true true true false false testImages
./makeElement.sh exists "Exists in Legacy" checkbox 1 true true true false false testImages
./makeElement.sh surrounding "Surrounding Landuse" dropdown 1 true true true false false testImages
./makeElement.sh surface "Surface Landuse" dropdown 1 true true true false false testImages
./makeElement.sh visibility "Visbility" dropdown 1 true true true false false testImages
./makeElement.sh latlong "latlong" latlong 1 true true true false false testImages
./makeElement.sh notes "notes" input 1 true true true false false testImages
./makeElement.sh takeShape "Take a Shape" button 1 true true true false false testImages
./makeElement.sh generalPhoto "General Photos" camera 1 true true true false false testImages
./makeElement.sh takePhoto "Take a Photo" button 1 true true true false false testImages

./makeElement.sh profile "Profile" pictureGallery 1 true true true false false testImages
./makeElement.sh plan "plan" pictureGallery 1 true true true false false testImages
./makeElement.sh lengthmax "Length Max" input 2 true true true false false testImages
./makeElement.sh lengthmin "Length Min" input 2 true true true false false testImages
./makeElement.sh widthmax "Width Max" input 2 true true true false false testImages
./makeElement.sh widthmin "Width Min" input 2 true true true false false testImages
./makeElement.sh heightmax "Height Max" input 2 true true true false false testImages
./makeElement.sh heightmin "Height Min" input 2 true true true false false testImages
./makeElement.sh areamax "Area Max" input 2 true true true false false testImages
./makeElement.sh areamin "Area Min" input 2 true true true false false testImages
./makeElement.sh otherdim "Other Dimension" input 1 true true true false false testImages
./makeElement.sh dimnotes "Dimension Notes" input 1 true true true false false testImages

./makeElement.sh attachSketch "Attach a Sketch" button 1 true true true false false testImages
./makeElement.sh viewSketch "View Attached Files" button 1 true true true false false testImages
./makeElement.sh listSketch "List of Attached Files" file 1 true true true false false testImages

./makeElement.sh dimensionPhoto "Dimension Photos" camera 1 true true true false false testImages
./makeElement.sh takeSketchPhoto "Take a Photo of Sketch" button 1 true true true false false testImages

./makeElement.sh featurePresent "Stone feature present and visible?" radio 1 true true true false false testImages
./makeElement.sh featureDesc "Stone feature description" input 1 true true true false false testImages
./makeElement.sh surfaceDense "Surface material density" dropdown 1 true true true false false testImages
./makeElement.sh surfaceDesc "Surface material description" input 1 true true true false false testImages
./makeElement.sh sampleColl "Sample Colelcted?" radio 1 true true true false false testImages

./makeElement.sh materialPhoto "Material Photos" camera 1 true true true false false testImages
./makeElement.sh takematerialPhoto "Take a Photo of Material" button 1 true true true false false testImages

./makeElement.sh disturbanceKind "Disturbance Kind" dropdown 1 true true true false false testImages
./makeElement.sh disturbanceFactors "Disturbance Factors" checkbox 1 true true true false false testImages
./makeElement.sh principalFactors "Principal Factors" dropdown 1 true true true false false testImages
./makeElement.sh ageOfDamage "Age of Damage" checkbox 1 true true true false false testImages
./makeElement.sh disturbanceDesc "disturbance description" input 1 true true true false false testImages
./makeElement.sh RTKind "RT Kind" checkbox 1 true true true false false testImages
./makeElement.sh RTMethod "RT Method" checkbox 1 true true true false false testImages
./makeElement.sh RTFrequency "RT Frequency" pictureGallery 1 true true true false false testImages
./makeElement.sh RTDesc "RT description" input 1 true true true false false testImages
./makeElement.sh VolumeofsoilremovedviaRT "Volume of soil removed via RT" dropdown 1 true true true false false testImages
./makeElement.sh Affect "Affect" dropdown 1 true true true false false testImages
./makeElement.sh Impact "Impact" dropdown 1 true true true false false testImages
./makeElement.sh CommentsandRecommendations "Comments and Recommendations" input 1 true true true false false testImages

./makeElement.sh CRMPhoto "CRM Photos" camera 1 true true true false false testImages
./makeElement.sh takeCRMPhoto "Take a Photo of CRM" button 1 true true true false false testImages
cd testImages

dot -Tpdf ../datastruct.gv > ../output.pdf

cd ..


montage testImages/*.svg -geometry +10+10 -border 2 -tile 4 -background lightgreen  allTestImages.pdf &

