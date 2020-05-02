import bpy
import bmesh 

import numpy as np
from scipy.sparse import coo_matrix


class Geometry:
    """
    
    Works on a manifold triangle mesh. 
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

    """
    
    def __init__(self):
        """
        
        """
        
        me = bpy.context.object.data
        self.bm = bmesh.new()
        bm.from_mesh(me)
        
        # This must be called to be able to iterate over mesh elements
        # Make sure to call again after adding/removing data in these sequences
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        
    
    def __del__(self):
        bm.free()
        
    
    def cotan(self, e, f):
        """
        Computes the cotangent of the angle opposite of given edge
        
        Args:
            e (bmesh.types.BMEdge): Edge opposite to angle we are looking for cotan of.
            f (bmesh.types.BMFace): Face the angle is located on.
            
        Returns:
            float: The cotangent of the angle. 
        """
        
        ## Check that the edge e is on the face f. 
        for edge in f.edges:
            if (e == edge):
                break
            else:
                raise ValueError('Edge e must be on face f')
        
        # v1 and v2 are the vertices at the ends of the edge e. 
        v1 = e.verts[0]
        v2 = e.verts[1]

        # v is the vertex that completes the face f with v1 and v2. 
        for vert in f.verts:
            if (vert != v1 and vert != v2):
                v = vert
        
        # A and B are the vectors of the edges adjacent to the angle we want
        # to compute the cotangent of. 
        A = v1.co - v.co
        B = v2.co - v.co
        
        ## Compute the cross and dot products of the edges adjacent to angle theta
        dot = A.dot(B)
        cross_norm = A.cross(B).length
        
        ## Return the cotangent of the angle
        return dot / cross_norm
        
        
        
    def cotan_laplace_matrix(self): 
        """
        Builds a sparse matrix encoding the Laplace-Beltrami operator for this mesh
        
        This implementation uses the cotan formula as the discrete Laplacian. 
        
        Returns: 
            coo_matrix: The sparse matrix encoding the Laplace-Beltrami operator
        """
        
        # numpy arrays used to construct final matrix
        row  = np.array([])
        col  = np.array([])
        data = np.array([])
        
        # variables
        n = len(bm.verts)
        
        ## Construct Laplacian matrix
        for i in range(n):
            ## Compute the Laplacian at each vertex
            Lu_ii = 0
            v_i = bm.verts[i]
            
            for e in v_i.link_edges:
                v_j = e.other_vert(v_i)
                f1 = e.link_faces[0]
                f2 = e.link_faces[1]
                Lu_ij = -0.5 * (self.cotan(e, f1) + self.cotan(e, f2)
                
                # Add to the matrix
                row  = row.append(v_i.index)
                col  = col.append(v_j.index)
                data = data.append(Lu_ij)
                
                Lu_ii -= Lu_ij
                
            row  = row.append(v_i.index)
            col  = col.append(v_i.index)
            data = data.append(Lu_ii + 1e-8)

        return coo_matrix((data, (row, col)), shape=(n, n))



class TestPanel(bpy.types.Panel):
    bl_label = "Test Panel"
    bl_idname = "TestPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NewTab"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text = "Sample Text", icon="CUBE")
        
        
def register():
    bpy.utils.register_class(TestPanel)
    
    
def unregister():
    bpy.utils.unregister_class(TestPanel)
    


    
if __name__=="__main__":
    register()
    print("Hello")
    
    
    
    
    bm.to_mesh(me)
    bm.free()
    


