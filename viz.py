#  Title: viz.py
#  Abstract: This program will render a audio visualization of an audio file. This program 
#            requires Blender. (Available blender.org: Open Source Software)
#  Author: Jeremy Gutierrez
#  ID: 9043
#  Date: 04/30/2015
#  Test Input: audio file
#  Test Output: Visualization of 36 cubes that move to audio frequencies of the audio file.
#
import bpy
import math

#This function creates the skin color and material for each object.
def makeMaterial(name, diffuse, specular, alpha): 
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse  #Diffuse the color applied
    mat.diffuse_shader = 'TOON'  #Use the Toon Shading Scheme
    mat.diffuse_intensity = 1.0  #Intensity set to max 1
    mat.specular_color = specular #Use to set hardnes of color 
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0 #0.5 Set intensity to 0 
    mat.alpha = alpha
    mat.ambient = 1
    return mat
 
# This will apply the created material to each object
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

#Delete all cube objects, Used to clear display area.
for ob in bpy.context.scene.objects:
    ob.select = ob.type == 'MESH' and ob.name.startswith("Cube") #Select all mesh cube objects
bpy.ops.object.delete() #delete all selected objects.

rows = 6 # max # of rows 
columns = 6 # max # of collumns
 
r = 0 #Row Counter
c = 0 #Collumn Counter
factor = 6 # Used in determining distances of blocks
for i in range(12):#For each row
    factor +=1
    for i in range(36): #For each collumn of blocks
        if c == columns:
            r +=1     #row count
            c = 0     #column count
        a = i/factor*3.141592654 #Setting of the x, y positions for each cube
        x = math.sin(a) * factor
        y = math.cos(a) * factor
        bpy.ops.mesh.primitive_cube_add(location=(x,y,0)) #Add each cube
        cur = bpy.context.scene.cursor_location
        cur.x = x
        cur.y = y
        cur.z = -1
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.transform.resize(value=(1,1,math.sin(a*5)*5+6))
        bpy.ops.transform.rotate(value=a-3.141592654*0.5)
        bpy.context.scene.cursor_location = bpy.context.active_object.location
        bpy.context.scene.cursor_location.z -= 1
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR') # Set the cursor to new location and place the cube there  
        bpy.context.active_object.scale.x = .5 #Setting the scale base values of each block dimensions
        bpy.context.active_object.scale.y = .5
        bpy.context.active_object.scale.z = 6
        bpy.ops.object.transform_apply(scale=True) #Cubes will be animated
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        bpy.context.active_object.animation_data.action.fcurves[0].lock = True #Lock the x & y, Movement occurs on z axis
        bpy.context.active_object.animation_data.action.fcurves[1].lock = True
        bpy.context.area.type = 'GRAPH_EDITOR' #Change to the graph editor to bake the sound to the animation
        step = 8000 / (rows*columns)
        thecolor = makeMaterial('Color',((step/2000),(step/4000)+(c/11),(step/6000)+(c/20)),(1,1,1),1) #Creates object color based on step and column
        setMaterial(bpy.context.object, thecolor) #Sets object color
        #This will select the sound file to use in creating the animation
        bpy.ops.graph.sound_bake(filepath="/blender/blended/unforgiven.mp3", low=i*step, high=i*step + step)
        bpy.context.active_object.animation_data.action.fcurves[2].lock = True #Lock the z axis, so it remains scaled to song
        c += 1     #Adds one to the column count
     
scene = bpy.data.scenes["Scene"] #Create the scene/animation
#Sets a variable as the current scene
bpy.context.scene.frame_end = 500 #Ending Fram 6mins:15seconds = 9000 frames, Set the Length of the song/animation. 500 set for testing
scene.camera.location.x += 10 #sets the position of the camera 
scene.camera.location.y -= 2
scene.camera.location.z += 2