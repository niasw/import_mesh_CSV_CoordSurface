bl_info = {
    'name': 'CSV CoordSurface',
    'category': 'Import-Export',
    'author': 'Sun Smallwhite <niasw@pku.edu.cn>',
    'location': 'File > Import > CSV CoordSurface UV -> XYZ mesh (.csv)',
    'description': 'Transfer coordinates data into new mesh surface',
    'version': (1, 0, 0),
    'blender': (2, 80, 0),
    'wiki_url': 'https://github.com/niasw/import_mesh_CSV_CoordSurface',
    'tracker_url': 'https://github.com/niasw/import_mesh_CSV_CoordSurface/issues',
    'warning': '',
}

import bpy
import csv
from bpy_extras import object_utils
from bpy.props import (
    StringProperty,
    EnumProperty
)
from mathutils import (
    Vector
)
from bpy_extras.io_utils import (
    ImportHelper
)

class ImportCSVCoordsSurface(bpy.types.Operator, ImportHelper):
    """Import CSV"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "import_mesh.csvcoordssurface"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Import CSV Data Surface (UV -> XYZ Coordinates)"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    filepath: StringProperty(
        name="input file",
        subtype='FILE_PATH'
    )

    filename_ext = ".csv"
    filter_glob: StringProperty(default="*.csv", options={'HIDDEN'})

    loop_mode: EnumProperty(
        name="Loop",
        items=(
            ('off', "No Loop", "Free boundary."),
            ('uLoop', "Loop for U", "Contact boundary at ends of U coordinate."),
            ('uLoopMobius', "Mobius for U", "Contact boundary at ends of U coordinate, but reverse V coordinate."),
            ('vLoop', "Loop for V", "Contact boundary at ends of V coordinate."),
            ('vLoopMobius', "Mobius for V", "Contact boundary at ends of V coordinate, but reverse U coordinate."),
            ('uvLoop', "Loop for U and V", "Contact boundaries at ends of U and V coordinates."),
        ),
    )

    def execute(self, context):        # execute() is called when running the operator.

        # The original script
        filename = self.filepath
        csvdata = loadCSV(filename)
        (verts, edges, faces)=weaveSurface(context, csvdata, self.loop_mode)
        createMeshObj(context, verts, edges, faces, "CoordSurface")

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def loadCSV(filename,delimiter=',',skiprows=0,skipcols=0):
    f=None;
    ret=None;
    try:
        f=open(filename,'r');
        reader=csv.reader(f,delimiter=delimiter);
        current_row=0;
        while (current_row<skiprows):
            current_row+=1;
            ret_row=next(reader);
        ret=[]
        for row in reader:
            ret_tmp=[float(it) for it in row[skipcols:]];
            ret.append(ret_tmp);
    except Exception as e:
        raise(e);
    finally:
        if f is not None:
            f.close();
    return ret;

def loadCSV_whitespace(filename,skiprows=0,skipcols=0):
    fileobj=None;
    try:
        fileobj=open(filename,'r');
        data=fileobj.readlines();
    finally:
        if fileobj is not None:
            fileobj.close()
    num=len(data);
    ret=[];
    for it in range(skiprows,num):
        row=data[it].split();
        ret_tmp=[float(da) for da in row[skipcols:]];
        ret.append(ret_tmp);
    return ret;

def createMeshObj(context, verts, edges, faces, meshname):
    mesh=bpy.data.meshes.new(meshname)
    mesh.from_pydata(verts,edges,faces)
    mesh.use_auto_smooth=False
    mesh.update()

    if (bpy.context.mode=="EDIT_MESH"):
        bpy.ops.object.mode_set(mode='OBJECT')

    return object_utils.object_data_add(context,mesh)

def weaveSurface(context, csvdata, loop_mode):
    verts=[]
    edges=[]
    faces=[]
    
    verts_num=len(csvdata)
    _u_last=None
    _u_idx=-1
    _v_idx=0
    surf_idx=[]
    row_idx=[]
    fst_row_idx=[]
    lst_row_idx=[]
    fst_col_idx=[]
    lst_col_idx=[]
    
    for it in range(0,verts_num):
        _u=csvdata[it][0]
        _v=csvdata[it][1]
        _x=csvdata[it][2]
        _y=csvdata[it][3]
        _z=csvdata[it][4]
        if (not (_u==_u_last)):
            _u_idx+=1
            if (_u_idx>0):
                lst_col_idx.append(it-1)
                surf_idx.append(row_idx)
                row_idx=[]
            fst_col_idx.append(it)
            _v_idx=0
        else:
            _v_idx+=1
            if (_u_idx>0):
                if (len(surf_idx[_u_idx-1])>_v_idx):
                    faces.append([surf_idx[_u_idx-1][_v_idx],surf_idx[_u_idx-1][_v_idx-1],row_idx[_v_idx-1],it])
                else:
                    faces.append([surf_idx[_u_idx-1][-1],row_idx[_v_idx-1],it])
        row_idx.append(it)
        _u_last=_u
        verts.append(Vector((_x,_y,_z)))

    lst_col_idx.append(len(verts)-1)
    surf_idx.append(row_idx)

    fst_row_idx=surf_idx[0]
    lst_row_idx=surf_idx[-1]

    if (loop_mode=="uLoop"):
        faces.extend(weave_line(fst_row_idx,lst_row_idx))
    elif (loop_mode=="vLoop"):
        faces.extend(weave_line(fst_col_idx,lst_col_idx))
    elif (loop_mode=="uLoopMobius"):
        lst_row_idx.reverse()
        faces.extend(weave_line(fst_row_idx,lst_row_idx))
    elif (loop_mode=="vLoopMobius"):
        lst_col_idx.reverse()
        faces.extend(weave_line(fst_col_idx,lst_col_idx))
    elif (loop_mode=="uvLoop"):
        faces.extend(weave_line(fst_row_idx,lst_row_idx))
        fst_col_idx.append(fst_col_idx[0])
        lst_col_idx.append(lst_col_idx[0])
        faces.extend(weave_line(fst_col_idx,lst_col_idx))

    if (len(faces)==0):
        for it in range(1,verts_num):
            edges.append([it-1,it])
        if (verts_num>1 and (loop_mode=="uLoop" or loop_mode=="vLoop" or loop_mode=="uvLoop" or loop_mode=="uLoopMobius" or loop_mode=="vLoopMobius")):
            edges.append([verts_num-1,0])

    return (verts, edges, faces);

def weave_line(fst_idx_list, lst_idx_list):
    new_faces=[]
    if (len(fst_idx_list)>=len(lst_idx_list)):
        for it in range(1,len(fst_idx_list)):
            if (it<len(lst_idx_list)):
                new_faces.append([lst_idx_list[it-1],lst_idx_list[it],fst_idx_list[it],fst_idx_list[it-1]])
            else:
                new_faces.append([lst_idx_list[-1],fst_idx_list[it],fst_idx_list[it-1]])
    else:
        for it in range(1,len(lst_idx_list)):
            if (it<len(fst_idx_list)):
                new_faces.append([lst_idx_list[it-1],lst_idx_list[it],fst_idx_list[it],fst_idx_list[it-1]])
            else:
                new_faces.append([lst_idx_list[it-1],lst_idx_list[it],fst_idx_list[-1]])
    return new_faces

def menu_func(self, context):
    self.layout.operator(ImportCSVCoordsSurface.bl_idname, text=ImportCSVCoordsSurface.bl_label)

def register():
    bpy.utils.register_class(ImportCSVCoordsSurface)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(ImportCSVCoordsSurface)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)  # Removes the operator from the existing menu.

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
