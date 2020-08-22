from pymel.core import *
import pymel.util
import os


def batch(rigFile, animList, destPath):
    
    #Save current scene
    renameFile('tmp.ma')
    saveFile(force = True)

    #For each file in list:
    for animFile in animList:  

        print("Running with file {0}".format(animFile))     
        exportAnimation(rigFile, animFile, destPath)
            


def exportAnimation(rigFile, animFile, destPath):
    
        #Prep new scene
        newSceneName = prep_new_scene(rigFile, animFile, destPath)
        
        #Get list of origin joints using namespace
        rigJoints = get_joints_from_namespace('rig')

        #Get list of target joints using the original transform name
        animJoints = get_joints_from_namespace('anim')
        
        #Set start and end time for baking and constraining
        startTime = findKeyframe(animJoints[0], which = "first")
        endTime = findKeyframe(animJoints[0], which = "last")
        playbackOptions(min = startTime)
        playbackOptions(max = endTime)

        currentTime(startTime)
        
        #Link rigs together
        for animJoint in animJoints:
             
             #Find the target joint to constrain
             rigJoint = find_target_joint(animJoint, 'rig')
             
             try:
                 parentConstraint(animJoint, rigJoint, mo = True)
             except:
                 print("{0} does not exist!".format(rigJoint))
             

        #Bake animation on target joints
        bakeResults(
                    rigJoints,
                    simulation = True,
                    time = (startTime, endTime),
                    sampleBy = 1,
                    oversamplingRate = 1,
                    disableImplicitControl = True,
                    preserveOutsideKeys = True,
                    sparseAnimCurveBake = False,
                    removeBakedAnimFromLayer = False,
                    bakeOnOverrideLayer = False,
                    minimizeRotation = True,
                    controlPoints = False,
                    shape = True
                    )

        #Remove reference - Code snippet by Alejandro Zapata
        animRef = FileReference(namespace='anim')
        animRef.remove()
        
        #Save
        saveFile(force = True)


    
#Creates a new scene with namespaces
def prep_new_scene(rigPath, animPath, destPath):
    
    #New Scene
    newFile(force = True)

    #Getting variable strings for scene name
    rigPathDir, rigPathFile = os.path.split(rigPath)
    rigPathName, rigPathExt = os.path.splitext(rigPathFile)
    animPathDir, animPathFile = os.path.split(animPath)
    animPathName = os.path.splitext(animPathFile)[0]

    #Setting variable strings to create new path
    newSceneDir = destPath
    newSceneFile = "{0}_{1}{2}".format(rigPathName, animPathName, rigPathExt)
    newScenePath = "{0}/{1}".format(newSceneDir, newSceneFile)

    #Create new directory for scene path
    if not os.path.exists(newSceneDir):
        os.mkdir(newSceneDir)

    #Rename current file to scene path for saving
    renameFile(newScenePath)

    #Import rig file w rig namespace
    rigRef = createReference(rigPath,  ns = 'rig')
    
    #Import anim file w anim namespace
    animRef = createReference(animPath, ns = 'anim')

    if not rigRef or not animRef:

        error("One or more references is invalid.")
        
        return

#Gets joints based on argument namespace
def get_joints_from_namespace(ns):
    
    return ls("{0}:*".format(ns), type = "joint")
   
#Finds analogous joint between namespaces 
def find_target_joint(srcJoint, dstNs):
    
    jointName = srcJoint.name(stripNamespace = True)
    
    targetJoint = "{0}:{1}".format(dstNs, jointName)
    
    return targetJoint
     