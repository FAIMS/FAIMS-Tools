#!/bin/bash

./makeElement.sh style_orientation_orientation "horizontal" input 1 false false false false false .
./makeElement.sh style_even_layout_weight "1" input 1 false false false false false .
./makeElement.sh style_large_layout_weight "3" input 1 false false false false false .
./makeElement.sh User_User_Select_User "Select User" list 1 false false false false false .
./makeElement.sh User_User_Login "Login" button 1 false false false false false .
./makeElement.sh User_User_Yes "Yes" list 1 false false false false false .
./makeElement.sh Control_Main_Record_Interview "Record Interview" button 1 false false false false false .
./makeElement.sh Control_Main_GPS_Diagnostics "GPS Diagnostics" input 1 false false false false true .
./makeElement.sh Control_Search_Search_Term "Search Term" input 2 false false false false false .
./makeElement.sh Control_Search_Search_Button "Search" button 2 false false false false false .
./makeElement.sh Control_Search_Entity_Types "Entity Types" dropdown 1 false false false false false .
./makeElement.sh Control_Search_Entity_List "Entity List" list 1 false false false false false .
./makeElement.sh Control_Search_Search_Term "Search Term" input 2 false false false false false .
./makeElement.sh Control_Search_Search_Button "Search" button 2 false false false false false .
./makeElement.sh Control_Search_Entity_Types "Entity Types" dropdown 1 false false false false false .
./makeElement.sh Control_Search_Entity_List "Entity List" list 1 false false false false false .
./makeElement.sh Test_Test_Tech "Tech" input 1 false false true false false .
./makeElement.sh Test_Test_Daybe_1 "Daybe 1" input 4 false false true false false .
./makeElement.sh Test_Test_Daybe_2 "Daybe 2" input 4 false false true false false .
./makeElement.sh Test_Test_Maybe_1 "Maybe 1" input 4 false false true false false .
./makeElement.sh Test_Test_Maybe_2 "Maybe 2" input 4 false false true false false .
./makeElement.sh Test_Test_Maybe_3 "Maybe 3" input 4 false false true false false .
./makeElement.sh Test_Test_Ceebe_1 "Ceebe 1" input 4 false false true false false .
./makeElement.sh Test_Test_Nutha_1 "Nutha 1" input 4 false false true false false .
./makeElement.sh Test_Test_Evening "Evening" input 1 false false true false false .
./makeElement.sh Interview_Interview_Timestamp "Timestamp" input 1 false false true false false .
./makeElement.sh Interview_Interview_Title "Title" input 1 false false true true false .
./makeElement.sh Interview_Interview_Description "Description" input 1 false false true true false .
./makeElement.sh Interview_Interview_Private "Private" radio 1 false false true true false .
./makeElement.sh Interview_Interview_Origination_Date "Origination Date" input 1 false false true true false .
./makeElement.sh Interview_Interview_Origination_Date_Narrative "Origination Date Narrative" input 1 false false true false false .
./makeElement.sh Interview_Interview_Add_Agent_Role "Add Agent Role" button 1 false false false false false .
./makeElement.sh Interview_Interview_List_of_Agent_Roles "List of Agent Roles" dropdown 1 false false false false false .
./makeElement.sh Interview_Interview_Linguistic_Data_Type "Linguistic Data Type" dropdown 1 false false true false false .
./makeElement.sh Interview_Interview_Discourse_Type "Discourse Type" dropdown 1 false false true false false .
./makeElement.sh Interview_Interview_Linguistic_Subject "Linguistic Subject" dropdown 1 false false true false false .
./makeElement.sh Interview_Interview_Country "Country" dropdown 1 false false true true false .
./makeElement.sh Interview_Interview_Region_Villiage "Region Villiage" dropdown 1 false false true false false .
./makeElement.sh Interview_Interview_Language_Local_Name "Language Local Name" dropdown 1 false false true false false .
./makeElement.sh Interview_Interview_Language_Content_ISO639-3 "Language Content ISO639-3" dropdown 1 false false true false false .
./makeElement.sh Interview_Interview_Language_Subject_ISO639-3 "Language Subject ISO639-3" dropdown 1 false false true false false .
./makeElement.sh Interview_Interview_Attached_Audio "Attached Audio" file 1 false false true false false .
./makeElement.sh Interview_Interview_Button_Attached_Audio "" button 1 false false false false false .
./makeElement.sh Interview_Interview_Attached_Video "Attached Video" file 1 false false true false false .
./makeElement.sh Interview_Interview_Button_Attached_Video "" button 1 false false false false false .
./makeElement.sh Agent_Role_Agent_Role_First_Name "First Name" input 1 false false true false false .
./makeElement.sh Agent_Role_Agent_Role_Last_Name "Last Name" input 1 false false true false false .
./makeElement.sh Agent_Role_Agent_Role_Role "Role" pictureGallery 1 false false true false false .

dot -Tsvg datastruct.gv > wireframe.svg
#rm *.xml
#rm *.datastruct.gv
#rm *.wireframeElements.sh

