## CSV CoordSurface (CSV坐标曲面：逗号分隔矢量数据文件(CSV)的坐标曲面导入插件)

### ----- (DataSurface for Blender 3.0) (原DataSurface的Blender3.0适用版)
### ----- (Transfer coordinates data into new mesh surface) (将坐标数据导入为新的网格曲面)

by Sun Sibai <niasw@pku.edu.cn> 作者 孙思白



### Motivation 动机

Since Blender has changed a lot from 2.6 to 3.0, the addon DataSurface I wrote for 2.6 is no longer working in 3.0. The main cause of compatibility problem is in 2.8 version update. However, the requirement is still there. Therefore I rewrite a new DataSurface addon here, naming it CSV CoordSurface. Besides, since API has been developed, I believe this new addon is much easier to use than the old DataSurface.

因为Blender从2.6到3.0变化很大，原来我针对2.6写的数据导入插件DataSurface不再适用于3.0了。主要的原因是2.8的更新不再兼容以前的插件书写框架。但是缺少这类插件，需求总是摆在那的。于是我重写了一个新的DataSurface插件，命名为CSV CoordSurface (CSV坐标曲面)。由于相应的接口也有更新，于是顺便重写使其更易于使用。




For versions Blender 2.6 to 2.7, please check <https://github.com/niasw/add_mesh_DataSurface>.

如果需要Blender 2.6到2.7的对应插件，请移步
<https://github.com/niasw/add_mesh_DataSurface>.



### What this addon is used for? 这个插件是干嘛用的？

For those who have not known my DataSurface addon in 2.6, I shall explain it again here. DataSurface is used for transferring coordinates data into corresponding mesh surface. To visualize data generated from experiments or mathematical calculations, this addon will help you to import those data into blender and generate the corresponding surface. Normally, vertices on a surface can be named by two dimensional coordinates (u,v). By giving the relationship between (u,v) and Descartes coordinates (x,y,z)=(x(u,v), y(u,v), z(u,v)), the surface is determined. Thus the input csv is formatted as 5 columns: u, v, x, y, z, where u and v can be integers as indices of vertices. 

如果你没听说过我的给2.6版本写的DataSurface插件，那么我这里介绍一下其思路。DataSurface插件用于将坐标数据转化为对应的网格面形。这个插件可以帮你导入由实验或者数学计算得到的数据至Blender中并且产生对应的曲面，以将这些数据可视化。一般来说，曲面上的格点可以由一组二维坐标(u,v)来标识确定。通过给出(u,v)和直角坐标系(x,y,z)=(x(u,v),y(u,x),z(u,v))的关系，可以唯一地确定这个曲面。因此作为输入的.csv文件的格式是5列数：u, v, x, y, z，其中u和v可以用整数比如格点的编号。



For example, a x-y plain square is imported if the input is:

0, 0, 0.0, 0.0, 0.0

0, 1, 0.0, 1.0, 0.0

1, 0, 1.0, 0.0, 0.0

1, 1, 1.0, 1.0, 0.0

Take the second row as an example, the second row denotes a point whose nametag as (u,v)=(0,1), and whose Descartes coordinates as (x,y,z)=(0.0, 1.0, 0.0)

比方说，一个x-y平面上的正方形可以由以下输入导入：

0, 0, 0.0, 0.0, 0.0

0, 1, 0.0, 1.0, 0.0

1, 0, 1.0, 0.0, 0.0

1, 1, 1.0, 1.0, 0.0

以其中第二行为例，文件中第二行指示了一个点，其标识为(u,v)=(0,1)，而其直角坐标为(x,y,z)=(0.0, 1.0, 0.0)




The purpose of using (x,y,z)=(x(u,v), y(u,v), z(u,v)) rather than the simplest z=z(x,y) is to describe surfaces bending across Descartes coordinates system axes, for example, a sphere, torus or mobius ribbon.

使用(x,y,z)=(x(u,v), y(u,v), z(u,v))而不使用最简单的z=z(x,y)的原因是为了可以描述一些弯曲穿过了直角坐标轴的曲面，比如说一个球、环或者莫比乌斯带。




### How to use this? 如何使用这个插件？

1. enable this addon 开启插件

* click 'Edit' > 'Preference...' in Menu 点菜单中的'编辑' > '偏好设置...'

* click 'Addon' on the left 点左边的'插件'栏

* click 'Install...' button and select the 'import_mesh_CSV_CoordSurface.py' file in this addon, install it 点'安装...'按钮，然后选择插件源码中的'import_mesh_CSV_CoordSurface.py'文件并安装

* click the 'Community' tag on the left side of the 'Install...' button 点'安装...'按钮左侧的'社区版'栏

* type "CSV CoordSurface" in the searchbar on the right side 在右边的搜索框中写"CSV CoordSurface"

* click the checkbox of CSV CoordSurface addon in the search results 勾选搜索结果中CSV CoordSurface插件前面的框框

2. use this addon 使用插件

* click 'File' > 'Import' > 'Import CSV Data CoordSurface (UV -> XYZ Coordinates) (.csv)' 点'文件' > '导入' > 'Import CSV Data CoordSurface (UV -> XYZ Coordinates) (.csv)'

* select the csv file which stores coordinates, import it 选择存坐标数据的.csv文件并导入



### Options 选项

​	You can import the simplest example 'example_2x2hill.csv' to check difference in these mode.

* no Loop

​	The simplest import, no furthur post-build process. The result surface will have four sides, namely u_min, v_min, u_max and v_max.

* u Loop

​	Loop in u coordinate. Contact u_min with u_max. The result surface will have two sides.

* v Loop

​	Loop in v coordinate. Contact v_min with v_max. The result surface will have two sides.

* uv Loop

​	 Loop in both u and v coordinates. The surface will cut the space into two separated parts, namely inside and outside. For a specific example, you can import 'example_hearttorus.csv' in this mode.

* u Loop Mobius

​	 Loop in u coordinate. contact u_min with u_max, but the v at contacting boundary is reversed. The result will make the surface have only one side. For a specific example, you can import 'example_mobius.csv' in this mode.

* v Loop Mobius

​	 Loop in v coordinate. contact v_min with v_max, but the u at contacting boundary is reversed. The result will make the surface have only one side.




​	你可以导入最简单的例子 'example_2x2hill.csv' 来查看不同选项模式带来的区别。

* noLoop

​	最简单的导入模式，没有任何后续处理。最终曲面会有四条边，即 u最小、v最小、u最大 和 v最大。

* uLoop

​	在u坐标上循环。将 u最小 和 u最大 连接。最终曲面会有两条边。

* vLoop

​	在v坐标上循环。将 v最小 和 v最大 连接。最终曲面会有两条边。

* uvLoop

​	 u坐标和v坐标都循环。曲面会将整个空间分割成两个互不连通的部分，即内部和外部。你可以以这个模式导入 'example_hearttorus.csv' 作为例子参考。

* uLoopMobius

​	在u坐标上循环。将 u最小 和 u最大 连接，但连接边界处v坐标相反。最终的后果会使曲面只有一条边。你可以以这个模式导入 'example_mobius.csv' 作为例子参考。

* vLoopMobius

​	在v坐标上循环。将 v最小 和 v最大 连接，但连接边界处u坐标相反。最终的后果会使曲面只有一条边。


### Dependency 前置依赖

* The main file 'import_mesh_CSV_CoordSurface.py' needs Blender, whose version should be 2.80 and above.

* The example generating files in Example directory do not need Blender, but need numpy. I am using version 1.16.4, but other versions may also work.

  

* 主程序 'import_mesh_CSV_CoordSurface.py' 需要2.80版本以上的Blender。

* Example文件夹中的生成例子的程序不需要Blender，但是需要numpy包。我用的是1.16.4版的，其他版本应该也可以正常工作。

