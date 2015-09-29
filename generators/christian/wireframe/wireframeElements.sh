
rmdir -rf wireframeImages/
mkdir -p wireframeImages


  ./makeElement.sh style_orientation_orientation "horizontal" input 1 false false false false false wireframeImages/
  
  ./makeElement.sh style_even_layout_weight "1" input 1 false false false false false wireframeImages/
  
  ./makeElement.sh style_large_layout_weight "3" input 1 false false false false false wireframeImages/
  
  ./makeElement.sh User_User_Select_User "Select User" list 1 false false false false false wireframeImages/
  
  ./makeElement.sh Control_Control_New_Ent "New Ent" button 1 false false false false false wireframeImages/
  
  ./makeElement.sh Control_Search_Search_Term "Search Term" input 2 false false false false false wireframeImages/
  
  ./makeElement.sh Control_Search_Search_Button "Search" button 2 false false false false false wireframeImages/
  
  ./makeElement.sh Control_Search_Entity_List "Entity List" list 1 false false false false false wireframeImages/
  
  ./makeElement.sh Ent_Tab_ID "ID" input 1 false false true false false wireframeImages/
  
  ./makeElement.sh Ent_Tab_Muh_Table "Muh Table" table 1 false false false false false wireframeImages/
  
  ./makeElement.sh Ent_Tab_Device_List "Device List" dropdown 1 false false false false false wireframeImages/
  
  ./makeElement.sh Ent_Tab_Refresh_List "Refresh List" button 1 false false false false false wireframeImages/
  