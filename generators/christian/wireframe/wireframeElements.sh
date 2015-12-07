
rmdir -rf wireframeImages/
mkdir -p wireframeImages


  ./makeElement.sh style_orientation_orientation "horizontal" input 1 false false false false false wireframeImages/
  
  ./makeElement.sh style_even_layout_weight "1" input 1 false false false false false wireframeImages/
  
  ./makeElement.sh style_large_layout_weight "3" input 1 false false false false false wireframeImages/
  
  ./makeElement.sh Tabgroup_Tab_Dummy "Dummy" input 1 false false true false false wireframeImages/
  
  ./makeElement.sh Tabgroup_Tab_Dropdown "Dropdown" dropdown 1 false false true false false wireframeImages/
  
  ./makeElement.sh Tabgroup_Tab_List "List" list 1 false false true false false wireframeImages/
  
  ./makeElement.sh Tabgroup_Tab_Picture "Picture" pictureGallery 1 false false true false false wireframeImages/
  
  ./makeElement.sh Tabgroup_Tab_Radio "Radio" radio 1 false false true false false wireframeImages/
  