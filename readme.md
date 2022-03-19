## CSV CoordSurface

### ----- (DataSurface for Blender 3.0)
### ----- (Transfer coordinates data into new mesh surface)

by Sun Sibai <niasw@pku.edu.cn>



### Motivation

Since Blender has changed a lot from 2.6 to 3.0, the addon DataSurface I wrote for 2.6 is no longer working in 3.0. The main cause of compatibility problem is in 2.8 version update. However, the requirement is still there. Therefore I rewrite a new DataSurface addon here, naming it CSV CoordSurface. Besides, since API has been developed, I believe this new addon is much easier to use than the old DataSurface.




### What this addon is used for?

For those who have not known my DataSurface addon in 2.6, I shall explain it again here. DataSurface is used for transferring coordinates data into corresponding mesh surface. To visualize data generated from experiments or mathematical calculations, this addon will help you to import those data into blender and generate the corresponding surface. Normally, vertices on a surface can be named by two dimensional coordinates (u,v). By giving the relationship between (u,v) and Descartes coordinates (x,y,z)=(x(u,v), y(u,v), z(u,v)), the surface is determined. Thus the input csv is formatted as 5 columns: u, v, x, y, z, where u and v can be integers as indices of vertices. 

For example, a x-y plain square is imported if the input is:

0, 0, 0.0, 0.0, 0.0

0, 1, 0.0, 1.0, 0.0

1, 0, 1.0, 0.0, 0.0

1, 1, 1.0, 1.0, 0.0

Take the second row as an example, the second line denotes a point whose nametag as (u,v)=(0,1), and whose Descartes coordinates as (x,y,z)=(0.0, 1.0, 0.0)

The purpose of using (x,y,z)=(x(u,v), y(u,v), z(u,v)) rather than the simplest z=z(x,y) is to describe surfaces bending across Descartes coordinates system axes, for example, a sphere, torus or mobius ribbon.



### How to use this?

1. enable this addon

* click 'Edit' > 'Preference' in Menu

* click 'Install...' button and select the 'import_mesh_CSV_CoordSurface.py' file in this addon, install it

* click the 'Community' tag on the left side of the 'Install...' button

* type "CSV CoordSurface" in the searchbar on the right side

* click the checkbox of CSV CoordSurface addon in the search results

2. use this addon

* click 'File' > 'Import' > 'CSV CoordSurface UV -> XYZ mesh (.csv)'

* select the csv file which stores coordinates, import it



### Options

​	You can import the simplest example 'example_2x2hill.csv' to check difference in these mode.

* no Loop

​	The simplest import. The result surface will have four sides, namely u_min, v_min, u_max and v_max.

* u Loop

 	Loop in u coordinate. Contact u_min with u_max. The result surface will have two sides.

* v Loop

​	Loop in v coordinate. Contact v_min with v_max. The result surface will have two sides.

* uv Loop

​	 Loop in both u and v coordinates. The surface will cut the space into two separated parts, namely inside and outside. For a specific example, you can import 'example_hearttorus.csv' in this mode.

* u Loop Mobius

​	 Loop in u coordinate. contact u_min with u_max, but the v at contacting boundary is reversed. The result will make the surface have only one side. For a specific example, you can import 'example_mobius.csv' in this mode.

* v Loop Mobius

​	 Loop in v coordinate. contact v_min with v_max, but the u at contacting boundary is reversed. The result will make the surface have only one side.



### Dependency

* The main file 'import_mesh_CSV_CoordSurface.py' needs Blender, whose version should be 2.80 and above.

* The example generating files in Example directory do not need Blender, but need numpy. I am using version 1.16.4, but other versions may also work.



