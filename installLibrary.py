# 
# 1) Locate Blender's local python. 
#       >>> bpy.app.binary_path_python
#       '/Your/Path/To/2.8x/python/bin/python3.7m'
#
# 2) cd to the bin directory.
#       $ cd /Your/Path/To/2.8x/python/bin/
# 
# 3) Since pip is shipped with blender 2.81+, just need to run ensurepip
#       $ ./python3.7m -m ensurepip   
# 
# 4) Update pip
#       $ ./python3.7m -m pip install -U pip
#
# 5) Install your package
#       $ ./python3.7m -m pip install scipy 
# 
# That's it! 
# 


import bpy
import subprocess
import ensurepip

ensurepip.bootstrap()

try:
    output = subprocess.call([bpy.app.binary_path_python, '-m', 'pip', 'install', 'scipy'])
    print(output)
    print("done")
except subprocess.CalledProcessError as e:
    print(e.output)
    print("Failed")
