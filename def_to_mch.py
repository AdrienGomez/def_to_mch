import bpy

# This script duplicate selected bones in edit mode, add duplicate bones to the 'mch' bone collection, then add a Copy Transform constraint to the first selected bones with the duplicated bones as target.

#bones must have 'def_' as suffix  in their names

#bones must be in edit_mode



#store selected bones
bonesel = bpy.context.selected_editable_bones

# create a fone name list for later
bonenamelist = []

#add selected bones names to list and rename them 
for defbone in bonesel:
    bonenamelist.append(defbone.name.replace('def', 'mch'))

#Duplicate selected bones  
bpy.ops.armature.duplicate_move()

#store the duplicated bones
newbonesel = bpy.context.selected_editable_bones

#rename the duplicated bones
for mchbone in newbonesel:
    i=0
    mchbone.name = bonenamelist[i]
    i+=1
    
#assign bones the duplicated bones to 'mch' Bone collections
bpy.ops.armature.collection_assign(name="mch")
#remove bones the duplicated bones from'def' Bone collections
bpy.ops.armature.collection_unassign(name="def")
#Deselect all bones   
bpy.ops.armature.select_all(action='DESELECT')
 
#select the first selected bones and select them
for defbone in bonesel:
   
    bpy.context.object.data.edit_bones[defbone.name].select = True

#switch to pose mode
bpy.ops.object.posemode_toggle()

#create a list with selected bones in pose mode
posebonesel = bpy.context.selected_pose_bones

#deselect all
bpy.ops.pose.select_all(action='DESELECT')

#for each bone in the selection, add a Copy Transform bone constraint with the duplicated bone as target
for posebone in posebonesel:
    bpy.context.object.data.bones[posebone.name].select = True
    bpy.context.object.data.bones.active = bpy.context.object.data.bones[posebone.name]
    bpy.ops.pose.constraint_add(type='COPY_TRANSFORMS')
    posebone.constraints["Copy Transforms"].target = bpy.context.object
    posebone.constraints["Copy Transforms"].subtarget = posebone.name.replace('def', 'mch')
    bpy.ops.pose.select_all(action='DESELECT')


### go back to initial selection and mode ###
#go back to edit mode    
bpy.ops.object.editmode_toggle()

#deselect all bone
bpy.ops.armature.select_all(action='DESELECT')

#select the first selected bones
for defbone in bonesel:   
    bpy.context.object.data.edit_bones[defbone.name].select = True



