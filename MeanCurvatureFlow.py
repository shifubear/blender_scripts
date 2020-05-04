import bpy

import sys 
sys.path.append('/Users/shion_fukuzawa/Desktop/ComputerGraphics/Blender/Scripts')

from Geometry import Geometry
from scipy import linalg


class MeanCurvatureFlowOperator(bpy.types.Operator):
    bl_idname = "wm.mean_curvature_flow"
    bl_label = "Integrate"

    def execute(self, context):
        mcf = MeanCurvatureFlow()
        mcf.integrate(0.005)

        print("New MCF Operator!!!!")
        return {'FINISHED'}


class MeanCurvatureFlow:
    """
    
    """
    
    def __init__(self):
        self.geom = Geometry()
        self.M = self.geom.mass_matrix()
        
    
    def build_flow_operator(self, h):
        """
        
        """
        
        A = self.geom.cotan_laplace_matrix()        
        return self.M + (h * A) 
    
    
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
    
    
if __name__=="__main__":
    mcf = MeanCurvatureFlow()
    mcf.integrate(0.005)

    
    bpy.utils.register_class(MeanCurvatureFlowOperator)

    # test call to the newly defined operator
    bpy.ops.wm.mean_curvature_flow()