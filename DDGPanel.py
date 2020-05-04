import bpy
import bmesh 

import numpy as np
from scipy import linalg


# Add sys path to scripts so they can be imported
import sys
sys.path.append('/Users/shion_fukuzawa/Desktop/ComputerGraphics/Blender/Scripts')

# Add DDG scripts
#from MeanCurvatureFlow import MeanCurvatureFlowOperator
#from MeanCurvatureFlow import MeanCurvatureFlow

from Geometry import Geometry

class MeanCurvatureFlow:
    """
    
    """
    
    def __init__(self):
        self.geom = Geometry()
        self.M = self.geom.mass_matrix()
        self.A = self.geom.cotan_laplace_matrix() 
        
    
    def build_flow_operator(self, h):
        """
        
        """  
        return self.M + (h * self.A) 
    
    
    def integrate(self, h): 
        """
        
        """
        
        n = len(self.geom.bm.verts)
        
        F = self.build_flow_operator(h)
        
        ## Create n x 3 matrix for RHS 
        f0 = []
        for v in self.geom.bm.verts:
            pos = [v.co.x, v.co.y, v.co.z]
            f0.append(pos)
        
        RHS = self.M.toarray().dot(f0)
        
        ## 
        L = linalg.cholesky(F.toarray(), lower=True)
        
        ## Solve linear system using LLT
        fh = linalg.cho_solve((L, True), RHS)

        
        for i in range(n): 
            self.geom.bm.verts[i].co.x = fh[i][0]
            self.geom.bm.verts[i].co.y = fh[i][1]
            self.geom.bm.verts[i].co.z = fh[i][2]
            
        self.geom.update()
    

MCF = MeanCurvatureFlow()


class MeanCurvatureFlowOperator(bpy.types.Operator):
    bl_idname = "wm.mean_curvature_flow"
    bl_label = "Integrate"

    def execute(self, context):
        MCF.integrate(0.005)
        print("MCFO")
        print("New MCF Operator!!!!")
        return {'FINISHED'}


class DDGPanel(bpy.types.Panel):
    bl_label = "DDG Panel"
    bl_idname = "OBJECT_PT_DDGPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DDG"
    
    
    def draw(self, context):
        layout = self.layout
        print("DDGPanel")
        row = layout.row()
        row.label(text = "Mean Curvature Flow", icon="META_CUBE")

        row = layout.row()
        row.operator("wm.mean_curvature_flow")


        
def register():       
    print("REGISTER")
    bpy.utils.register_class(MeanCurvatureFlowOperator)  
    bpy.utils.register_class(DDGPanel)

    
def unregister():
    bpy.utils.unregister_class(DDGPanel)
    bpy.utils.unregister_class(MeanCurvatureFlowOperator)
        

if __name__=="__main__":
    print("MAIN")

    unregister()
    register()
    
#    me = bpy.context.object.data
    
#    bm = bmesh.new()
#    bm.from_mesh(me)
    
#    for v in bm.verts:
#        v.co.x += v.co.x
#        v.co.y += v.co.y
#        v.co.z += v.co.z
#    
#    bm.to_mesh(me)
#    bm.free()
    
  
#    unregister()
    
    



