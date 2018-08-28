'''
    NURB Limb
    Copyright (C) 2018-2019 Demonic Benefactor <demonic@tutanota.de>
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

from pyfbsdk import *
import os
NUM_MARKERS =   4

'''
# The FBMessageBoxGetUserValue is Terribad,   going to find another solution for input
#Get the amount of Controls from the user
request = FBMessageBoxGetUserValue( "Enter the number of Controls", "Amount: ", 4, FBPopupInputType.kFBPopupInt, "OK")
if request[0]:
    NUM_MARKERS = request[1]
    splinePOS   = 1 / ((NUM_MARKERS - 1) * 1.0)
else:
    # Or tell that there was an error...
    FBMessageBox( "Result", "Got an error", "Ok" )

del( request )
'''

def FindAnimationNode( pParent, pName ):
    lResult = None
    for lNode in pParent.Nodes:
        if lNode.Name == pName:
            lResult = lNode
            break
    return lResult

def BuildNURB(pBone, pCons, pTime, pMarkers, pPhase, pPosition, pCount, pTotal):
    lBoxTik = 0
    boxes = []
    curveOUT = False
    fromCurve = False
    boneBox = pCons.ConstrainObject(pBone)
    boxCount = len( pMarkers ) / 4
    boneMarkSync = int((pCount * 1.0) / (pPhase * 1.0)) * 4
    remainderBox = 0
    remMarkInd = 0
    if (len( pMarkers ) % 4) > 0:
        remainderBox = 1
   
    for lBox in range(boxCount + 1):
        if lBox < boxCount - 1 or lBox == boxCount - 1 and (len( pMarkers ) % 4) > 0:
            if curveOUT != False:
                fromCurve = curveOUT
                markersAdded = True
            curveBox = pCons.CreateFunctionBox( 'Other', 'Bezier Curve' )
            curveBox.Name = 'NURB to ' + str(pBone.Name) + '_' + str(lBoxTik)
            pCons.SetBoxPosition(curveBox, 300 + (lBox * 400), pCount * 200)
            print pCount
            boxes.append( curveBox )
            curveOUT = FindAnimationNode( curveBox.AnimationNodeOutGet(), 'Result')
            curveResultIN = FindAnimationNode( curveBox.AnimationNodeInGet(), "Previous Segment's Result")
            curveSegCountIN = FindAnimationNode( curveBox.AnimationNodeInGet(), "Segment Count")
            curveSegIndexIN = FindAnimationNode( curveBox.AnimationNodeInGet(), "Segment Index")
            curveSegCountIN.WriteData([boxCount + remainderBox])
            curveSegIndexIN.WriteData([lBoxTik + 1])
            if fromCurve != False:
                FBConnect(fromCurve, curveResultIN)            
            bonePosRat = FindAnimationNode( curveBox.AnimationNodeInGet(), 'Position Ratio [0, 100]')
            bonePosRat.WriteData([pPosition * pCount])

        elif lBox == boxCount:
            if curveOUT != False:
                fromCurve = curveOUT
                boxLoc = lBox
            else: boxLoc = -1
            curveBox = pCons.CreateFunctionBox( 'Other', 'Bezier Curve' )
            curveBox.Name = 'NURB to ' + str(pBone.Name) + '_' + str(lBoxTik)
            pCons.SetBoxPosition(curveBox, 300 + ((lBox + boxLoc) * 300), pCount * 200)
            boxes.append( curveBox )
            curveOUT = FindAnimationNode( curveBox.AnimationNodeOutGet(), 'Result')
            curveResultIN = FindAnimationNode( curveBox.AnimationNodeInGet(), "Previous Segment's Result")
            curveSegCountIN = FindAnimationNode( curveBox.AnimationNodeInGet(), "Segment Count")
            curveSegIndexIN = FindAnimationNode( curveBox.AnimationNodeInGet(), "Segment Index")
            curveSegCountIN.WriteData([boxCount + remainderBox])
            curveSegIndexIN.WriteData([lBoxTik + remainderBox])
            if fromCurve != False:
                FBConnect(fromCurve, curveResultIN)
            boneIN = FindAnimationNode( boneBox.AnimationNodeInGet(), 'Translation')
            pCons.SetBoxPosition(boneBox, 1600 + ((lBox + boxLoc) * 400), pCount * 200)
            if pCount == 0 or pCount == pTotal:
                FBConnect(curveOUT, boneIN)
            else:
                lPhsAdder = pCons.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
                lSin = pCons.CreateFunctionBox( 'Sources', 'Sine Ramp' )
                lNumToVec = pCons.CreateFunctionBox( 'Converters', 'Number to Vector' )
                lAddVec = pCons.CreateFunctionBox( 'Vector', 'Add (V1 + V2)' )
                pCons.SetBoxPosition(lSin, 850 + ((lBox + boxLoc) * 400 - 50), pCount * 200)
                pCons.SetBoxPosition(lPhsAdder, 850 + ((lBox + boxLoc) * 400 - 50), pCount * 200 -70)
                pCons.SetBoxPosition(lNumToVec, 950 + ((lBox + boxLoc) * 400 - 50), pCount * 200)
                pCons.SetBoxPosition(lAddVec, 1200 + ((lBox + boxLoc) * 400 - 50), pCount * 200)
                
                lMarkAmp = FindAnimationNode( pMarkers[0].AnimationNodeOutGet(), "WaveHeight")
                lMarkFreq = FindAnimationNode( pMarkers[0].AnimationNodeOutGet(), "Speed")
                lMarkDist = FindAnimationNode( pMarkers[0].AnimationNodeOutGet(), "WaveLength")
                
                lSinAmp = FindAnimationNode( lSin.AnimationNodeInGet(), "Amp")
                lSinFreq = FindAnimationNode( lSin.AnimationNodeInGet(), "Freq")
                lSinPhase = FindAnimationNode( lSin.AnimationNodeInGet(), "Phase %")
                lSinPlay = FindAnimationNode( lSin.AnimationNodeInGet(), "Play Mode")
                lSinResult = FindAnimationNode( lSin.AnimationNodeOutGet(), "Result")               
                lXIn = FindAnimationNode( lNumToVec.AnimationNodeInGet(), "X")
                lYIn = FindAnimationNode( lNumToVec.AnimationNodeInGet(), "Y")
                lZIn = FindAnimationNode( lNumToVec.AnimationNodeInGet(), "Z")
                lNtVResult = FindAnimationNode( lNumToVec.AnimationNodeOutGet(), "Result")
                lAddA = FindAnimationNode( lAddVec.AnimationNodeInGet(), "V1")
                lAddB = FindAnimationNode( lAddVec.AnimationNodeInGet(), "V2")
                lAddresult = FindAnimationNode( lAddVec.AnimationNodeOutGet(), "Result")
                lPhsInA = FindAnimationNode( lPhsAdder.AnimationNodeInGet(), "a")
                lPhsInB = FindAnimationNode( lPhsAdder.AnimationNodeInGet(), "b")
                lPhsResult = FindAnimationNode( lPhsAdder.AnimationNodeOutGet(), "Result")
                
                FBConnect( curveOUT, lAddB )
                FBConnect( lMarkAmp, lSinAmp )
                FBConnect( lMarkFreq, lSinFreq )
                
                FBConnect( lMarkDist, lPhsInA )
                lPhsInB.WriteData([pCount])
                FBConnect( lPhsResult, lSinPhase )
                
                FBConnect( pTime, lSinPlay )
                FBConnect( lSinResult, lXIn )
                FBConnect( lSinResult, lYIn )
                FBConnect( lSinResult, lZIn )
                FBConnect( lNtVResult, lAddA )
                FBConnect( lAddresult, boneIN )
                
            bonePosRat = FindAnimationNode( curveBox.AnimationNodeInGet(), 'Position Ratio [0, 100]')
            bonePosRat.WriteData([pPosition * pCount])        
        lBoxTik += 1
    #This wires the controls into the system.  The Ratio to Bones needs to be improved.
    for box in enumerate(boxes):
        if box[0] == len(boxes) -1 and len( pMarkers ) % 4 > 0:
            remMarkInd = len(pMarkers) - (boxCount * 4)
        for i in range(4):
            markerOUT = FindAnimationNode( pMarkers[i + ((box[0] * 4) - remMarkInd )].AnimationNodeOutGet(), 'Translation' )
            curveControlIN = FindAnimationNode( box[1].AnimationNodeInGet(), "Control Point " + str(i + 1))
            FBConnect( markerOUT, curveControlIN )

#localize everything in a main function for cleanup
def main():
    splinePOS   = 1 / ((NUM_MARKERS - 1) * 1.0)
    it          =   0.0    
    app         =   FBApplication()
    constraint  =   FBConstraintRelation("NurbLimb")
    constraint.Active = True
    sysTime    =   constraint.CreateFunctionBox( 'System', 'System Time' )
    timeToSec  =   constraint.CreateFunctionBox( 'Converters', 'Time to Seconds' )
    timeBox    =   FindAnimationNode( sysTime.AnimationNodeOutGet(), 'Result')
    toSecBox   =   FindAnimationNode( timeToSec.AnimationNodeInGet(), 'Time')
    secBoxOut  =   FindAnimationNode( timeToSec.AnimationNodeOutGet(), 'Result')
    FBConnect( timeBox, toSecBox )
    constraint.SetBoxPosition(sysTime, 0, -50)
    constraint.SetBoxPosition(timeToSec, 200, -50)
        
    
    system      =   FBSystem()
    scene       =   system.Scene

    selection   =   FBModelList()
    bones       =   FBModelList()
    markers   =   []
    matrix      =   FBMatrix()
    vector      =   FBVector3d()
    FBGetSelectedModels( selection )
            
    #Get a handle on the bones in the selection.
    for obj in selection:
        if obj.FbxGetObjectSubType() == 'FBModelSkeleton':
            bones.append( obj )            

    #Get some vector data for calculation
    if bones.GetCount() <= 3:
        print 'not enough bones selected'      
        return 
    else:
        firstBonePOS    =   FBVector3d()
        lastBonePOS     =   FBVector3d()
        firstBoneROT    =   FBVector3d()
        lastBoneROT     =   FBVector3d()
        bones[0].GetVector( firstBonePOS, FBModelTransformationType.kModelTranslation, True  )
        bones[0].GetVector( firstBoneROT, FBModelTransformationType.kModelRotation, True )
        bones[bones.GetCount() - 1].GetVector( lastBonePOS, FBModelTransformationType.kModelTranslation, True  )
        bones[bones.GetCount() - 1].GetVector( lastBoneROT, FBModelTransformationType.kModelRotation, True )
        dirPOS = lastBonePOS - firstBonePOS
        lenPOS = dirPOS.Length()
        dirROT = lastBoneROT - firstBoneROT
        lenROT = dirROT.Length()
    
    #Create our control handles and position them
    for control in range(NUM_MARKERS):
        marker = FBModelMarker( 'NurbHandle'+ str( control ) )
        markerBox = constraint.SetAsSource( marker )
        constraint.SetBoxPosition(markerBox, 10, control * 150)
        markers.append( markerBox )
        marker.Visibility = True
        marker.Show = True
        marker.Size = 360
        if ( control == 0 ):
            lWavPr = marker.PropertyCreate('WaveHeight', FBPropertyType.kFBPT_int, 'Number', True, True, None )
            lFreqPr = marker.PropertyCreate('Speed', FBPropertyType.kFBPT_int, 'Number', True, True, None )
            lLenPr = marker.PropertyCreate('WaveLength', FBPropertyType.kFBPT_int, 'Number', True, True, None )
            lWavPr.SetAnimated( True )
            lWavPr.SetMax( 20 )
            lFreqPr.SetAnimated( True )
            lFreqPr.SetMax( 2 )
            lLenPr.SetAnimated( True )
            lLenPr.SetMax( 100 )
            marker.Size = 500
        vector = dirPOS.Normalize() * (lenPOS * it)
        marker.SetVector( firstBonePOS + vector, FBModelTransformationType.kModelTranslation, True  )
        vector = dirROT.Normalize() * (lenROT * it)
        marker.SetVector( firstBoneROT + vector, FBModelTransformationType.kModelRotation, True )
        it += splinePOS    
        
    
    #Curve setup
    markerPhase = abs(round((bones.GetCount() * 1.0) / (len(markers) * 0.25)))
    for bone in enumerate(bones):
        BuildNURB(bone[1], constraint, secBoxOut, markers, markerPhase, 
                    (1 / ((bones.GetCount() -1 ) * 1.0)) * 100, bone[0], bones.GetCount() -1)

        
               
main()
del NUM_MARKERS