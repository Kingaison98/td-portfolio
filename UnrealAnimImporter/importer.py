import unreal
import glob, os

'''

# need skeleton path
skeleton = unreal.load_asset("/Game/character/Mesh/character_skeleton")

# need animation source path
anim_source_path = r'Y:\IntroToTechArt\wk05\sample_file\AAA_0050_tk01.fbx'.replace("\\", "/")

# need animation destination
anim_dest_path = "/Game/character/Animations"

'''

def batch(skeleton_path, anim_dir, dest_dir):
    #Verify skeleton is valid
    if not skeleton_path or not unreal.EditorAssetLibrary.does_asset_exist(skeleton_path):

        print("No skeleton found")
        return

    #Verify anim directory is valid, if not, return
    if not os.path.exists(anim_dir):

        print("Need a list of animations.")
        return

    #Verify destination is valid, if not, make the directory (or prompt user if you want to make the directory)
    if not os.path.exists(dest_dir):

        print("Creating destination directory {0}".format(dest_dir))
        os.mkdir(dest_dir)

    
    #Loading skeleton and getting name for logging
    skeleton_name = skeleton_path.split("/")[-1]
    skeleton = unreal.EditorAssetLibrary.load_asset(skeleton_path)

    
    anim_dir_files = os.listdir(anim_dir)
    anim_list = []

    #Adds all .fbx files to list to be exported
    for file in anim_dir_files:
        if file.endswith(".fbx"):
            anim_list.append(file)

    for anim in anim_list:

        print("Importing: {0} to {1} on {2} rig".format(anim, dest_dir, skeleton_name))
        import_animation(skeleton, anim, dest_dir)
    

'''
Function by Greg Richardson
'''
def import_animation(skeleton, anim_source_path, anim_dest_path):

    # Animation section
    anim_seq_import_data = unreal.FbxAnimSequenceImportData()
    anim_seq_import_data.set_editor_property("animation_length", unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    anim_seq_import_data.set_editor_property("convert_scene", True)
    anim_seq_import_data.set_editor_property("use_default_sample_rate", True)
    anim_seq_import_data.set_editor_property("import_bone_tracks", True)
    anim_seq_import_data.set_editor_property("import_meshes_in_bone_hierarchy", False)
    anim_seq_import_data.set_editor_property("import_custom_attribute", False)
    anim_seq_import_data.set_editor_property("do_not_import_curve_with_zero", False)
    anim_seq_import_data.set_editor_property("remove_redundant_keys", False)

    # FBX Import UI options
    ui_import_options = unreal.FbxImportUI()
    ui_import_options.reset_to_default()
    ui_import_options.set_editor_property("automated_import_should_detect_type", False)
    ui_import_options.set_editor_property("import_animations", True)
    ui_import_options.set_editor_property("import_as_skeletal", False)
    ui_import_options.set_editor_property("import_rigid_mesh", False)
    ui_import_options.set_editor_property("import_materials", False)
    ui_import_options.set_editor_property("import_mesh", False)
    ui_import_options.set_editor_property("import_textures", False)
    ui_import_options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    ui_import_options.set_editor_property("skeleton", skeleton)
    ui_import_options.set_editor_property("anim_sequence_import_data",anim_seq_import_data)

    # Create Import task
    asset_import_task = unreal.AssetImportTask()
    asset_import_task.set_editor_property("automated", True)
    asset_import_task.set_editor_property("destination_path",anim_dest_path)
    asset_import_task.set_editor_property("filename",anim_source_path)
    asset_import_task.set_editor_property("options",ui_import_options)
    asset_import_task.set_editor_property("save", True)

    tasks = [asset_import_task]

    # Run import task
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    #asset_tools.import_asset_tasks(tasks)
 
    unreal.AssetTools.import_asset_tasks(asset_tools, tasks)