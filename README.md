# GPX Data to ShapeFiles
Takes a folder of GPX data from a GPS and converts tracks to lines. Additionally, 
it appends Origins and Destinations to separate feature classes. 

User needs to create a Line, Origin, and Destination Feature class prior to running script 
so each file can be appended to them easily. When creating the Feature Classes, create 
attributes that will have the same attributes/names as the input GPX data.
