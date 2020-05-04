import bpy
import bmesh 

import numpy as np
from scipy import linalg

class TestPanel(bpy.types.Panel):
    bl_label = "Test Panel"
    bl_idname = "OBJECT_PT_TestPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NewTab"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text = "Sample Text", icon="CUBE")
        
        row = layout.row()
        row.operator("wm.hello_world")

class HelloWorldOperator(bpy.types.Operator):
    bl_idname = "wm.hello_world"
    bl_label = "Minimal Operator"

    def execute(self, context):
        print("Hello World")
        return {'FINISHED'}

        
def register():
    bpy.utils.register_class(TestPanel)
    
    
def unregister():
    bpy.utils.unregister_class(TestPanel)
    

if __name__=="__main__":
    register()
    print("Hello")
    
        
#    bpy.utils.register_class(HelloWorldOperator)

#    # test call to the newly defined operator
#    bpy.ops.wm.hello_world()
    
#    me = bpy.context.object.data
#    
#    bm = bmesh.new()
#    bm.from_mesh(me)
#    
#    for v in bm.verts:
#        v.co.x += v.co.x
#        v.co.y += v.co.y
#        v.co.z += v.co.z
#    
#    bm.to_mesh(me)
#    bm.free()
    


