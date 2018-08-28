'''
    FBBox LookAt
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
    
    This is an FBBox conversion of the following lookat code which in turn
    is a Matrix-less GLUT/GLM style lookAt()
    
    Quaternion LookRotation(vec3 forward, vec3 up)
    {
        forward = forward.Normalize();
 
        vec3 vector = forward.Normalize();
        vec3 vector2 = up.CrossProduct(vector).Normalize();
        vec3 vector3 = vector.CrossProduct(vector2);
        float m00 = vector2.X;
        float m01 = vector2.Y;
        float m02 = vector2.Z;
        float m10 = vector3.X;
        float m11 = vector3.Y;
        float m12 = vector3.Z;
        float m20 = vector.X;
        float m21 = vector.Y;
        float m22 = vector.Z;
 
        float num8 = (m00 + m11) + m22;
        Quaternion quat;

        if (num8 > 0.0)
        {
            float num = (double)Math.Sqrt(num8 + 1.0);
            quat.w = num * 0.5;
            num = 0.5 / num;
            quat.x = (m12 - m21) * num;
            quat.y = (m20 - m02) * num;
            quat.z = (m01 - m10) * num;
            return quat;
        }
        if ((m00 >= m11) && (m00 >= m22))
        {
            float num7 = (double)Math.Sqrt(((1.0 + m00) - m11) - m22);
            float num4 = 0.5 / num7;
            quat.x = 0.5 * num7;
            quat.y = (m01 + m10) * num4;
            quat.z = (m02 + m20) * num4;
            quat.w = (m12 - m21) * num4;
            return quat;
        }
        if (m11 > m22)
        {
            float num6 = (double)Math.Sqrt(((1.0 + m11) - m00) - m22);
            float num3 = 0.5 / num6;
            quat.x = (m10 + m01) * num3;
            quat.y = 0.5 * num6;
            quat.z = (m21 + m12) * num3;
            quat.w = (m20 - m02) * num3;
            return quat;
        }
        float num5 = (double)Math.Sqrt(((1.0 + m22) - m00) - m11);
        float num2 = 0.5 / num5;
        quat.x = (m20 + m02) * num2;
        quat.y = (m21 + m12) * num2;
        quat.z = 0.5 * num5;
        quat.w = (m01 - m10) * num2;
        return quat;
    }
    
'''

from pyfbsdk import *

def FindAnimationNode( pParent, pName ):
    lResult = None
    for lNode in pParent.Nodes:
        if lNode.Name == pName:
            lResult = lNode
            break
    return lResult

def ShowAnimationNodes( pParent ):
    for lNode in pParent.Nodes:
        print lNode.Name


def toEulerAngle():
    for i in FBSystem().Scene.Constraints:
        if ( i.Name == "#toEulerAngle" ):
            i.FBDelete()
    #Make the inputs for a quaternion WXYZ            
    constraint  =   FBConstraintRelation("#toEulerAngle")
    macInW = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Input Number' )
    macInX = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Input Number' )
    macInY = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Input Number' )
    macInZ = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Input Number' )
    macInW.Name = 'W'
    macInX.Name = 'X'
    macInY.Name = 'Y'
    macInZ.Name = 'Z'
    constraint.SetBoxPosition( macInW, 0, 0 )
    constraint.SetBoxPosition( macInX, 0, 50 )
    constraint.SetBoxPosition( macInY, 0, 100 )
    constraint.SetBoxPosition( macInZ, 0, 150 )
    #Evaluate Euler X from quaternion
    WxX = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    YxZ = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    WxXpYxZ = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    WxXpYxZx = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    XxX = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    YxY = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    XxXpYxY = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    XxXpYxYx = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    XxXpYxYxs = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    atanTwoX = constraint.CreateFunctionBox( 'Number', 'arctan2(b/a)' )
    WxX.Name = 'W x X'
    YxZ.Name = 'Y x Z'
    WxXpYxZ.Name = 'W x X + Y x Z'
    WxXpYxZx.Name = 'WxX+YxZ x 2'
    XxX.Name = 'X x X'
    YxY.Name = 'Y x Y'
    XxXpYxY.Name = 'X x X + Y x Y'
    XxXpYxYx.Name = 'XxX+YxY x 2'
    XxXpYxYxs.Name = 'XxX+YxYx2-1'    
    constraint.SetBoxPosition( WxX, 180, 0 )
    constraint.SetBoxPosition( YxZ, 180, 60 )
    constraint.SetBoxPosition( WxXpYxZ, 440, 50 )
    constraint.SetBoxPosition( WxXpYxZx, 700, 20 )    
    constraint.SetBoxPosition( XxX, 180, 130 )
    constraint.SetBoxPosition( YxY, 180, 190 )
    constraint.SetBoxPosition( XxXpYxY, 440, 180 )
    constraint.SetBoxPosition( XxXpYxYx, 700, 150 )
    constraint.SetBoxPosition( XxXpYxYxs, 960, 200 )
    constraint.SetBoxPosition( atanTwoX, 1650, 300 )
    qWOut = FindAnimationNode( macInW.AnimationNodeOutGet(), "Input")
    qXOut = FindAnimationNode( macInX.AnimationNodeOutGet(), "Input")
    qYOut = FindAnimationNode( macInY.AnimationNodeOutGet(), "Input")
    qZOut = FindAnimationNode( macInZ.AnimationNodeOutGet(), "Input")
    WxXInA = FindAnimationNode( WxX.AnimationNodeInGet(), "a")
    WxXInB = FindAnimationNode( WxX.AnimationNodeInGet(), "b")
    WxXOut = FindAnimationNode( WxX.AnimationNodeOutGet(), "Result")
    YxZInA = FindAnimationNode( YxZ.AnimationNodeInGet(), "a")
    YxZInB = FindAnimationNode( YxZ.AnimationNodeInGet(), "b")
    YxZOut = FindAnimationNode( YxZ.AnimationNodeOutGet(), "Result")
    XxXInA = FindAnimationNode( XxX.AnimationNodeInGet(), "a")
    XxXInB = FindAnimationNode( XxX.AnimationNodeInGet(), "b")
    XxXOut = FindAnimationNode( XxX.AnimationNodeOutGet(), "Result")
    YxYInA = FindAnimationNode( YxY.AnimationNodeInGet(), "a")
    YxYInB = FindAnimationNode( YxY.AnimationNodeInGet(), "b")
    YxYOut = FindAnimationNode( YxY.AnimationNodeOutGet(), "Result")
    
    WxXpYxZInA = FindAnimationNode( WxXpYxZ.AnimationNodeInGet(), "a")
    WxXpYxZInB = FindAnimationNode( WxXpYxZ.AnimationNodeInGet(), "b")
    WxXpYxZOut = FindAnimationNode( WxXpYxZ.AnimationNodeOutGet(), "Result")
    XxXpYxYInA = FindAnimationNode( XxXpYxY.AnimationNodeInGet(), "a")
    XxXpYxYInB = FindAnimationNode( XxXpYxY.AnimationNodeInGet(), "b")
    XxXpYxYOut = FindAnimationNode( XxXpYxY.AnimationNodeOutGet(), "Result")
    
    WxXpYxZxInA = FindAnimationNode( WxXpYxZx.AnimationNodeInGet(), "a")
    WxXpYxZxInB = FindAnimationNode( WxXpYxZx.AnimationNodeInGet(), "b")
    WxXpYxZxOut = FindAnimationNode( WxXpYxZx.AnimationNodeOutGet(), "Result")
    XxXpYxYxInA = FindAnimationNode( XxXpYxYx.AnimationNodeInGet(), "a")
    XxXpYxYxInB = FindAnimationNode( XxXpYxYx.AnimationNodeInGet(), "b")
    XxXpYxYxOut = FindAnimationNode( XxXpYxYx.AnimationNodeOutGet(), "Result")
    
    XxXpYxYxsInA = FindAnimationNode( XxXpYxYxs.AnimationNodeInGet(), "a")
    XxXpYxYxsInB = FindAnimationNode( XxXpYxYxs.AnimationNodeInGet(), "b")
    XxXpYxYxsOut = FindAnimationNode( XxXpYxYxs.AnimationNodeOutGet(), "Result")
    
    atanTwoXInA = FindAnimationNode( atanTwoX.AnimationNodeInGet(), "a")
    atanTwoXInB = FindAnimationNode( atanTwoX.AnimationNodeInGet(), "b")
    atanTwoXOut = FindAnimationNode( atanTwoX.AnimationNodeOutGet(), "Result")
    
    FBConnect(qWOut, WxXInA)
    FBConnect(qXOut, WxXInB)
    FBConnect(qYOut, YxZInA)
    FBConnect(qZOut, YxZInB)
    FBConnect(qXOut, XxXInA)
    FBConnect(qXOut, XxXInB)
    FBConnect(qYOut, YxYInA)
    FBConnect(qYOut, YxYInB)
    FBConnect(WxXOut, WxXpYxZInA)
    FBConnect(YxZOut, WxXpYxZInB)
    FBConnect(XxXOut, XxXpYxYInA)
    FBConnect(YxYOut, XxXpYxYInB)
    
    FBConnect(WxXpYxZOut, WxXpYxZxInB)
    FBConnect(XxXpYxYOut, XxXpYxYxInB)
    WxXpYxZxInA.WriteData([2.0])
    XxXpYxYxInA.WriteData([2.0])
    
    FBConnect(WxXpYxZxOut, atanTwoXInB)
    FBConnect(XxXpYxYxOut, XxXpYxYxsInB)
    XxXpYxYxsInA.WriteData([1.0])
    FBConnect(XxXpYxYxsOut, atanTwoXInA)
    
    #Evaluate Euler Y from quaternion
    
    WxY = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    ZxX = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    WxYpZxX = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    WxYpZxXx = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    
    IfCondThenAElseBpos = constraint.CreateFunctionBox( 'Number', 'IF Cond Then A Else B' )
    IfCondThenAElseBneg = constraint.CreateFunctionBox( 'Number', 'IF Cond Then A Else B' )
    
    IsGreater = constraint.CreateFunctionBox( 'Number', 'Is Greater (a > b)' )
    IsLess = constraint.CreateFunctionBox( 'Number', 'Is Less (a < b)' )
    
    arcsin = constraint.CreateFunctionBox( 'Number', 'arcsin(a)' )
    
    
    WxY.Name = 'W x Y'
    ZxX.Name = 'Z x X'
    WxYpZxX.Name = 'W x Y - Z x X'
    WxYpZxXx.Name = 'W x Y - Z x X x 2'
    IfCondThenAElseBpos.Name = 'If CondThenAElseBpos'
    IfCondThenAElseBneg.Name = 'If CondThenAElseBneg'
    IsGreater.Name = 'Is Greater (a > b)'
    IsLess.Name = 'IsLess (a < b)'
    
    constraint.SetBoxPosition( WxY, 180, 400 )
    constraint.SetBoxPosition( ZxX, 180, 500 )
    constraint.SetBoxPosition( WxYpZxX, 460, 450 )
    constraint.SetBoxPosition( WxYpZxXx, 710, 395 )
    constraint.SetBoxPosition( IsGreater, 990, 500 )
    constraint.SetBoxPosition( IsLess, 970, 580 ) 
    constraint.SetBoxPosition( IfCondThenAElseBpos, 1070, 350 )
    constraint.SetBoxPosition( IfCondThenAElseBneg, 1370, 450 )    
    constraint.SetBoxPosition( arcsin, 1650, 450 )
    WxYInA = FindAnimationNode( WxY.AnimationNodeInGet(), "a")
    WxYInB = FindAnimationNode( WxY.AnimationNodeInGet(), "b")
    WxYOut = FindAnimationNode( WxY.AnimationNodeOutGet(), "Result")
    ZxXInA = FindAnimationNode( ZxX.AnimationNodeInGet(), "a")
    ZxXInB = FindAnimationNode( ZxX.AnimationNodeInGet(), "b")
    ZxXOut = FindAnimationNode( ZxX.AnimationNodeOutGet(), "Result")
    
    WxYpZxXInA = FindAnimationNode( WxYpZxX.AnimationNodeInGet(), "a")
    WxYpZxXInB = FindAnimationNode( WxYpZxX.AnimationNodeInGet(), "b")
    WxYpZxXOut = FindAnimationNode( WxYpZxX.AnimationNodeOutGet(), "Result")
    
    WxYpZxXxInA = FindAnimationNode( WxYpZxXx.AnimationNodeInGet(), "a")
    WxYpZxXxInB = FindAnimationNode( WxYpZxXx.AnimationNodeInGet(), "b")
    WxYpZxXxOut = FindAnimationNode( WxYpZxXx.AnimationNodeOutGet(), "Result")
    
    IsGreaterInA = FindAnimationNode( IsGreater.AnimationNodeInGet(), "a")
    IsGreaterInB = FindAnimationNode( IsGreater.AnimationNodeInGet(), "b")
    IsGreaterOut = FindAnimationNode( IsGreater.AnimationNodeOutGet(), "Result")
    IsLessInA = FindAnimationNode( IsLess.AnimationNodeInGet(), "a")
    IsLessInB = FindAnimationNode( IsLess.AnimationNodeInGet(), "b")
    IsLessOut = FindAnimationNode( IsLess.AnimationNodeOutGet(), "Result")
    
    IfCondThenAElseBposInA = FindAnimationNode( IfCondThenAElseBpos.AnimationNodeInGet(), "a")
    IfCondThenAElseBposInB = FindAnimationNode( IfCondThenAElseBpos.AnimationNodeInGet(), "b")
    IfCondThenAElseBposCond = FindAnimationNode( IfCondThenAElseBpos.AnimationNodeInGet(), "Cond")
    IfCondThenAElseBposOut = FindAnimationNode( IfCondThenAElseBpos.AnimationNodeOutGet(), "Result")
    IfCondThenAElseBnegInA = FindAnimationNode( IfCondThenAElseBneg.AnimationNodeInGet(), "a")
    IfCondThenAElseBnegInB = FindAnimationNode( IfCondThenAElseBneg.AnimationNodeInGet(), "b")
    IfCondThenAElseBnegCond = FindAnimationNode( IfCondThenAElseBneg.AnimationNodeInGet(), "Cond")
    IfCondThenAElseBnegOut = FindAnimationNode( IfCondThenAElseBneg.AnimationNodeOutGet(), "Result")
    
    arcsinInA = FindAnimationNode( arcsin.AnimationNodeInGet(), "a")
    arcsinInB = FindAnimationNode( arcsin.AnimationNodeInGet(), "b")
    arcsinOut = FindAnimationNode( arcsin.AnimationNodeOutGet(), "Result")
    
    FBConnect(qWOut, WxYInA)
    FBConnect(qXOut, ZxXInB)
    FBConnect(qYOut, WxYInB)
    FBConnect(qZOut, ZxXInA)
    
    FBConnect(WxYOut, WxYpZxXInA)
    FBConnect(ZxXOut, WxYpZxXInB)
    FBConnect(WxYpZxXOut, WxYpZxXxInB)
    FBConnect(WxYpZxXxOut, IfCondThenAElseBposInB)
    FBConnect(WxYpZxXxOut, IsGreaterInA)
    FBConnect(WxYpZxXxOut, IsLessInA)
    FBConnect(IsGreaterOut, IfCondThenAElseBposCond )
    FBConnect(IsLessOut, IfCondThenAElseBnegCond )
    FBConnect(IfCondThenAElseBposOut, IfCondThenAElseBnegInB )
    FBConnect(IfCondThenAElseBnegOut, arcsinInA )
    WxYpZxXxInA.WriteData([2.0])
    IfCondThenAElseBposInA.WriteData([1.0])
    IfCondThenAElseBnegInA.WriteData([-1.0])
    IsGreaterInB.WriteData([1.0])
    IsLessInB.WriteData([-1.0])
    
    #Evaluate Euler Z from quaternion
    
    WxZ = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    XxY = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    YxY = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    ZxZ = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    WxZpXxY = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    YxYpZxZ = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    WxZpXxYx = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    YxYpZxZx = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    YxYpZxZxs = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    atanTwoZ = constraint.CreateFunctionBox( 'Number', 'arctan2(b/a)' )
    
    WxZ.Name = 'W x Z'
    XxY.Name = 'X x Y'
    YxY.Name = 'Y x Y'
    ZxZ.Name = 'Z x Z'
    WxZpXxY.Name = 'W x Z + X x Y'
    YxYpZxZ.Name = 'Y x Y + Z x Z'
    WxZpXxYx.Name = 'W x Z + X x Y x 2'
    YxYpZxZx.Name = 'Y x Y + Z x Z x 2'
    YxYpZxZxs.Name = 'YxY+ZxZx2-1' 
    
    constraint.SetBoxPosition( WxZ, 180, 690 )
    constraint.SetBoxPosition( XxY, 180, 750 )
    constraint.SetBoxPosition( YxY, 180, 800 )
    constraint.SetBoxPosition( ZxZ, 180, 870 )
    constraint.SetBoxPosition( WxZpXxY, 440, 720 )
    constraint.SetBoxPosition( YxYpZxZ, 440, 835 )
    constraint.SetBoxPosition( WxZpXxYx, 700, 690 ) 
    constraint.SetBoxPosition( YxYpZxZx, 700, 800 )
    constraint.SetBoxPosition( YxYpZxZxs, 960, 750 )
    constraint.SetBoxPosition( atanTwoZ, 1650, 550 )
    
    qWOut = FindAnimationNode( macInW.AnimationNodeOutGet(), "Input")
    qXOut = FindAnimationNode( macInX.AnimationNodeOutGet(), "Input")
    qYOut = FindAnimationNode( macInY.AnimationNodeOutGet(), "Input")
    qZOut = FindAnimationNode( macInZ.AnimationNodeOutGet(), "Input")
    WxZInA = FindAnimationNode( WxZ.AnimationNodeInGet(), "a")
    WxZInB = FindAnimationNode( WxZ.AnimationNodeInGet(), "b")
    WxZOut = FindAnimationNode( WxZ.AnimationNodeOutGet(), "Result")
    XxYInA = FindAnimationNode( XxY.AnimationNodeInGet(), "a")
    XxYInB = FindAnimationNode( XxY.AnimationNodeInGet(), "b")
    XxYOut = FindAnimationNode( XxY.AnimationNodeOutGet(), "Result")
    YxYInA = FindAnimationNode( YxY.AnimationNodeInGet(), "a")
    YxYInB = FindAnimationNode( YxY.AnimationNodeInGet(), "b")
    YxYOut = FindAnimationNode( YxY.AnimationNodeOutGet(), "Result")
    ZxZInA = FindAnimationNode( ZxZ.AnimationNodeInGet(), "a")
    ZxZInB = FindAnimationNode( ZxZ.AnimationNodeInGet(), "b")
    ZxZOut = FindAnimationNode( ZxZ.AnimationNodeOutGet(), "Result")
    
    WxZpXxYInA = FindAnimationNode( WxZpXxY.AnimationNodeInGet(), "a")
    WxZpXxYInB = FindAnimationNode( WxZpXxY.AnimationNodeInGet(), "b")
    WxZpXxYOut = FindAnimationNode( WxZpXxY.AnimationNodeOutGet(), "Result")
    YxYpZxZInA = FindAnimationNode( YxYpZxZ.AnimationNodeInGet(), "a")
    YxYpZxZInB = FindAnimationNode( YxYpZxZ.AnimationNodeInGet(), "b")
    YxYpZxZOut = FindAnimationNode( YxYpZxZ.AnimationNodeOutGet(), "Result")
    
    WxZpXxYxInA = FindAnimationNode( WxZpXxYx.AnimationNodeInGet(), "a")
    WxZpXxYxInB = FindAnimationNode( WxZpXxYx.AnimationNodeInGet(), "b")
    WxZpXxYxOut = FindAnimationNode( WxZpXxYx.AnimationNodeOutGet(), "Result")
    YxYpZxZxInA = FindAnimationNode( YxYpZxZx.AnimationNodeInGet(), "a")
    YxYpZxZxInB = FindAnimationNode( YxYpZxZx.AnimationNodeInGet(), "b")
    YxYpZxZxOut = FindAnimationNode( YxYpZxZx.AnimationNodeOutGet(), "Result")
    
    YxYpZxZxsInA = FindAnimationNode( YxYpZxZxs.AnimationNodeInGet(), "a")
    YxYpZxZxsInB = FindAnimationNode( YxYpZxZxs.AnimationNodeInGet(), "b")
    YxYpZxZxsOut = FindAnimationNode( YxYpZxZxs.AnimationNodeOutGet(), "Result")
    
    atanTwoZInA = FindAnimationNode( atanTwoZ.AnimationNodeInGet(), "a")
    atanTwoZInB = FindAnimationNode( atanTwoZ.AnimationNodeInGet(), "b")
    atanTwoZOut = FindAnimationNode( atanTwoZ.AnimationNodeOutGet(), "Result")
    
    FBConnect(qWOut, WxZInA)
    FBConnect(qXOut, XxYInA)
    FBConnect(qYOut, XxYInB)
    FBConnect(qZOut, WxZInB)
    
    FBConnect(qZOut, ZxZInA)
    FBConnect(qZOut, ZxZInB)
    FBConnect(qYOut, YxYInA)
    FBConnect(qYOut, YxYInB)
    
    FBConnect(WxZOut, WxZpXxYInA)
    FBConnect(XxYOut, WxZpXxYInB)
    FBConnect(ZxZOut, YxYpZxZInA)
    FBConnect(YxYOut, YxYpZxZInB)
    
    FBConnect(WxZpXxYOut, WxZpXxYxInB)
    FBConnect(YxYpZxZOut, YxYpZxZxInB)
    FBConnect(YxYpZxZxOut, YxYpZxZxsInB)
    
    FBConnect(WxZpXxYxOut, atanTwoZInB)
    FBConnect(YxYpZxZxsOut, atanTwoZInA)
    
    WxZpXxYxInA.WriteData([2.0])
    YxYpZxZxInA.WriteData([2.0])
    YxYpZxZxsInA.WriteData([1.0])
    
    #Number to vector
    
    NtoV = constraint.CreateFunctionBox( 'Converters', 'Number to vector' )
    NtoV.Name = 'Number to Vector'
    
    NtoVInX = FindAnimationNode( NtoV.AnimationNodeInGet(), "X")
    NtoVInY = FindAnimationNode( NtoV.AnimationNodeInGet(), "Y")
    NtoVInZ = FindAnimationNode( NtoV.AnimationNodeInGet(), "Z")
    NtoVOut = FindAnimationNode( NtoV.AnimationNodeOutGet(), "Result")
    
    constraint.SetBoxPosition( NtoV, 1950, 450 )
    
    #Macro Output Vector
    
    MoutpV = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Output Vector' )
    MoutpV.Name = 'Macro Output Vector'
    
    MoutpVIn = FindAnimationNode( MoutpV.AnimationNodeInGet(), "Output")
    
    constraint.SetBoxPosition( MoutpV, 2250, 450 )
    
    FBConnect(atanTwoXOut, NtoVInX)
    FBConnect(arcsinOut, NtoVInY)
    FBConnect(atanTwoZOut, NtoVInZ)
    FBConnect(NtoVOut, MoutpVIn)

#################################################################################
#################################################################################
#################################################################################
#################################################################################

def lookAtMacro():
    for i in FBSystem().Scene.Constraints:
        if ( i.Name == "#lookAt" ):
            i.FBDelete()
    constraint = FBConstraintRelation("#lookAt")
    ##########################################
    # Construct our abstract rotation matrix #
    ##########################################
    macInCenter = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Input Vector' )
    macInEye = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Input Vector' )
    macInUp = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Input Vector' )
    macInAim = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Input Vector' )
    centerSEye = constraint.CreateFunctionBox( 'Vector', 'Subtract (V1 - V2)' )
    norDir = constraint.CreateFunctionBox( 'Vector', 'Normalize' )
    crossDir = constraint.CreateFunctionBox( 'Vector', 'Vector Product (V1 x V2)' )
    norSide = constraint.CreateFunctionBox( 'Vector', 'Normalize' )
    crossDirSide = constraint.CreateFunctionBox( 'Vector', 'Vector Product (V1 x V2)' )
    M0 = constraint.CreateFunctionBox( 'Converters', 'Vector to Number' )
    M1 = constraint.CreateFunctionBox( 'Converters', 'Vector to Number' )
    M2 = constraint.CreateFunctionBox( 'Converters', 'Vector to Number' )
    
    macInCenter.Name = 'Center'
    macInEye.Name = 'Eye'
    macInUp.Name = 'Up'
    macInAim.Name = 'AimOffset'
    centerSEye.Name = 'Center - Eye'
    norDir.Name = 'Normalize Direction'
    crossDir.Name = "Cross Direction Up"
    norSide.Name = 'Normalize Side'
    crossDirSide.Name = "Cross Direction Side"
    M0.Name = "M0"
    M1.Name = "M1"
    M2.Name = "M2"
    
    constraint.SetBoxPosition( macInCenter, 0, 0 )
    constraint.SetBoxPosition( macInEye, 0, 50 )
    constraint.SetBoxPosition( macInUp, 0, 100 )
    constraint.SetBoxPosition( macInAim, 2300, 500 )
    constraint.SetBoxPosition( centerSEye, 170, 10 )
    constraint.SetBoxPosition( norDir, 420, 10 )
    constraint.SetBoxPosition( crossDir, 170, 80 )
    constraint.SetBoxPosition( norSide, 420, 80 )
    constraint.SetBoxPosition( crossDirSide, 170, 150 )
    constraint.SetBoxPosition( M0, 700, 10 )
    constraint.SetBoxPosition( M1, 700, 100 )
    constraint.SetBoxPosition( M2, 700, 190 ) # Start at 170, 280
    
    macInCenterOut = FindAnimationNode( macInCenter.AnimationNodeOutGet(), "Input")
    macInEyeOut = FindAnimationNode( macInEye.AnimationNodeOutGet(), "Input")
    macInUpOut = FindAnimationNode( macInUp.AnimationNodeOutGet(), "Input")
    macInAimOut = FindAnimationNode( macInAim.AnimationNodeOutGet(), "Input")    
    centerSEyeInA = FindAnimationNode( centerSEye.AnimationNodeInGet(), "V1")
    centerSEyeInB = FindAnimationNode( centerSEye.AnimationNodeInGet(), "V2")
    centerSEyeOut = FindAnimationNode( centerSEye.AnimationNodeOutGet(), "Result")
    norDirIn  = FindAnimationNode( norDir.AnimationNodeInGet(), "Vector")
    norDirOut  = FindAnimationNode( norDir.AnimationNodeOutGet(), "Result")
    crossDirA = FindAnimationNode( crossDir.AnimationNodeInGet(), "V1")
    crossDirB = FindAnimationNode( crossDir.AnimationNodeInGet(), "V2")
    crossDirOut = FindAnimationNode( crossDir.AnimationNodeOutGet(), "Result")
    norSideIn  = FindAnimationNode( norSide.AnimationNodeInGet(), "Vector")
    norSideOut  = FindAnimationNode( norSide.AnimationNodeOutGet(), "Result")
    crossDirSideA = FindAnimationNode( crossDirSide.AnimationNodeInGet(), "V1")
    crossDirSideB = FindAnimationNode( crossDirSide.AnimationNodeInGet(), "V2")
    crossDirSideOut = FindAnimationNode( crossDirSide.AnimationNodeOutGet(), "Result")
    M0In = FindAnimationNode( M0.AnimationNodeInGet(), "V")
    M0X = FindAnimationNode( M0.AnimationNodeOutGet(), "X")
    M0Y = FindAnimationNode( M0.AnimationNodeOutGet(), "Y")
    M0Z = FindAnimationNode( M0.AnimationNodeOutGet(), "Z")
    M1In = FindAnimationNode( M1.AnimationNodeInGet(), "V")
    M1X = FindAnimationNode( M1.AnimationNodeOutGet(), "X")
    M1Y = FindAnimationNode( M1.AnimationNodeOutGet(), "Y")
    M1Z = FindAnimationNode( M1.AnimationNodeOutGet(), "Z")
    M2In = FindAnimationNode( M2.AnimationNodeInGet(), "V")
    M2X = FindAnimationNode( M2.AnimationNodeOutGet(), "X")
    M2Y = FindAnimationNode( M2.AnimationNodeOutGet(), "Y")
    M2Z = FindAnimationNode( M2.AnimationNodeOutGet(), "Z")
    
    FBConnect( macInCenterOut, centerSEyeInA )
    FBConnect( macInEyeOut, centerSEyeInB )
    FBConnect( centerSEyeOut, norDirIn )
    FBConnect( norDirOut, crossDirA )
    FBConnect( macInUpOut, crossDirB )
    FBConnect( crossDirOut, norSideIn )
    FBConnect( norDirOut, crossDirSideA )
    FBConnect( norSideOut, crossDirSideB )
    FBConnect( norSideOut, M0In )
    FBConnect( crossDirSideOut, M1In )
    FBConnect( norDirOut, M2In )
    
    #############################
    # Evaluate Quaternion Case1 #
    #############################
    C1_M22p1 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C1_M22p1sM00 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C1_M22p1sM00sM11 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C1_sqrt = constraint.CreateFunctionBox( 'Number', 'sqrt(a)' )
    C1_div1 = constraint.CreateFunctionBox( 'Number', 'Divide (a/b)' )
    C1_M01sM10 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C1_M20pM02 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C1_M21pM12 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C1_W = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C1_X = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C1_Y = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C1_Z = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C1_toEuler = constraint.CreateFunctionBox( 'My Macros', '#toEulerAngle' )
    
    C1_M22p1.Name = 'Case1 (1 + M2.Z)'
    C1_M22p1sM00.Name = 'Case1 (- M0.X)'
    C1_M22p1sM00sM11.Name = 'Case1 (- M1.Y)'
    C1_sqrt.Name = 'Case1 Sqrt()'
    C1_div1.Name = 'Case1 (a/b)'
    C1_M01sM10.Name = 'Case1 (M0.Y - M1.X)'
    C1_M20pM02.Name = 'Case1 (M2.X + M0.Z)'
    C1_M21pM12.Name = 'Case1 (M2.Y + M1.Z)'
    C1_W.Name = 'Case1 (x) W'
    C1_X.Name = 'Case1 (x) X'
    C1_Y.Name = 'Case1 (x) Y'
    C1_Z.Name = 'Case1 (x) Z'
    C1_toEuler.Name = 'Case1 Quaternion to Euler'
    
    
    constraint.SetBoxPosition( C1_M22p1, 170, 300 )
    constraint.SetBoxPosition( C1_M22p1sM00, 430, 300 )
    constraint.SetBoxPosition( C1_M22p1sM00sM11, 690, 300 )
    constraint.SetBoxPosition( C1_sqrt, 950, 300 )
    constraint.SetBoxPosition( C1_div1, 950, 350 ) 
    constraint.SetBoxPosition( C1_M01sM10, 950, 90 )
    constraint.SetBoxPosition( C1_M20pM02, 950, 160 )
    constraint.SetBoxPosition( C1_M21pM12, 950, 230 )
    constraint.SetBoxPosition( C1_W, 1250, 100 )
    constraint.SetBoxPosition( C1_X, 1250, 170 )
    constraint.SetBoxPosition( C1_Y, 1250, 240 )
    constraint.SetBoxPosition( C1_Z, 1250, 310 )
    constraint.SetBoxPosition( C1_toEuler, 1550, 80 )
        
    C1_M22p1A = FindAnimationNode( C1_M22p1.AnimationNodeInGet(), "a")
    C1_M22p1B = FindAnimationNode( C1_M22p1.AnimationNodeInGet(), "b")
    C1_M22p1Out = FindAnimationNode( C1_M22p1.AnimationNodeOutGet(), "Result")
    C1_M22p1sM00A = FindAnimationNode( C1_M22p1sM00.AnimationNodeInGet(), "a")
    C1_M22p1sM00B = FindAnimationNode( C1_M22p1sM00.AnimationNodeInGet(), "b")
    C1_M22p1sM00Out = FindAnimationNode( C1_M22p1sM00.AnimationNodeOutGet(), "Result")
    C1_M22p1sM00sM11A = FindAnimationNode( C1_M22p1sM00sM11.AnimationNodeInGet(), "a")
    C1_M22p1sM00sM11B = FindAnimationNode( C1_M22p1sM00sM11.AnimationNodeInGet(), "b")
    C1_M22p1sM00sM11Out = FindAnimationNode( C1_M22p1sM00sM11.AnimationNodeOutGet(), "Result")
    C1_sqrtIn = FindAnimationNode( C1_sqrt.AnimationNodeInGet(), "a")
    C1_sqrtOut = FindAnimationNode( C1_sqrt.AnimationNodeOutGet(), "Result")
    C1_div1A = FindAnimationNode( C1_div1.AnimationNodeInGet(), "a")
    C1_div1B = FindAnimationNode( C1_div1.AnimationNodeInGet(), "b")
    C1_div1Out = FindAnimationNode( C1_div1.AnimationNodeOutGet(), "Result")
    C1_M01sM10A = FindAnimationNode( C1_M01sM10.AnimationNodeInGet(), "a")
    C1_M01sM10B = FindAnimationNode( C1_M01sM10.AnimationNodeInGet(), "b")
    C1_M01sM10Out = FindAnimationNode( C1_M01sM10.AnimationNodeOutGet(), "Result")
    C1_M20pM02A = FindAnimationNode( C1_M20pM02.AnimationNodeInGet(), "a")
    C1_M20pM02B = FindAnimationNode( C1_M20pM02.AnimationNodeInGet(), "b")
    C1_M20pM02Out = FindAnimationNode( C1_M20pM02.AnimationNodeOutGet(), "Result")
    C1_M21pM12A = FindAnimationNode( C1_M21pM12.AnimationNodeInGet(), "a")
    C1_M21pM12B = FindAnimationNode( C1_M21pM12.AnimationNodeInGet(), "b")
    C1_M21pM12Out = FindAnimationNode( C1_M21pM12.AnimationNodeOutGet(), "Result")
    C1_WA = FindAnimationNode( C1_W.AnimationNodeInGet(), "a")
    C1_WB = FindAnimationNode( C1_W.AnimationNodeInGet(), "b")
    C1_WOut = FindAnimationNode( C1_W.AnimationNodeOutGet(), "Result")
    C1_XA = FindAnimationNode( C1_X.AnimationNodeInGet(), "a")
    C1_XB = FindAnimationNode( C1_X.AnimationNodeInGet(), "b")
    C1_XOut = FindAnimationNode( C1_X.AnimationNodeOutGet(), "Result")
    C1_YA = FindAnimationNode( C1_Y.AnimationNodeInGet(), "a")
    C1_YB = FindAnimationNode( C1_Y.AnimationNodeInGet(), "b")
    C1_YOut = FindAnimationNode( C1_Y.AnimationNodeOutGet(), "Result")
    C1_ZA = FindAnimationNode( C1_Z.AnimationNodeInGet(), "a")
    C1_ZB = FindAnimationNode( C1_Z.AnimationNodeInGet(), "b")
    C1_ZOut = FindAnimationNode( C1_Z.AnimationNodeOutGet(), "Result")
    C1_toEulerW = FindAnimationNode( C1_toEuler.AnimationNodeInGet(), "MacroInput0")
    C1_toEulerX = FindAnimationNode( C1_toEuler.AnimationNodeInGet(), "MacroInput1")
    C1_toEulerY = FindAnimationNode( C1_toEuler.AnimationNodeInGet(), "MacroInput2")
    C1_toEulerZ = FindAnimationNode( C1_toEuler.AnimationNodeInGet(), "MacroInput3")
    C1_toEulerOut = FindAnimationNode( C1_toEuler.AnimationNodeOutGet(), "MacroOutput0")
    
    C1_M22p1A.WriteData([1.0])
    FBConnect( M2Z, C1_M22p1B )
    FBConnect( C1_M22p1Out, C1_M22p1sM00A )
    FBConnect( M0X, C1_M22p1sM00B )
    FBConnect( C1_M22p1sM00Out, C1_M22p1sM00sM11A )
    FBConnect( M1Y, C1_M22p1sM00sM11B )
    FBConnect( C1_M22p1sM00sM11Out, C1_sqrtIn )
    C1_div1A.WriteData([0.5])
    FBConnect( C1_sqrtOut, C1_div1B )
    FBConnect( M0Y, C1_M01sM10A )
    FBConnect( M1X, C1_M01sM10B )
    FBConnect( M2X, C1_M20pM02A )
    FBConnect( M0Z, C1_M20pM02B )
    FBConnect( M2Y, C1_M21pM12A )
    FBConnect( M1Z, C1_M21pM12B )
    
    FBConnect( C1_M01sM10Out, C1_WA )
    FBConnect( C1_div1Out, C1_WB )
    FBConnect( C1_M20pM02Out, C1_XA )
    FBConnect( C1_div1Out, C1_XB )
    FBConnect( C1_M21pM12Out, C1_YA )
    FBConnect( C1_div1Out, C1_YB )
    C1_ZA.WriteData([0.5])
    FBConnect( C1_sqrtOut, C1_ZB )
    FBConnect( C1_WOut, C1_toEulerW )
    FBConnect( C1_XOut, C1_toEulerX )
    FBConnect( C1_YOut, C1_toEulerY )
    FBConnect( C1_ZOut, C1_toEulerZ )
    
    #############################
    # Evaluate Quaternion Case2 #
    #############################
    C2_M00pM11 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C2_M00pM11pM22 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' ) #This is the box we test against.
    C2_M00pM11pM22p1 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    
    C2_sqrt = constraint.CreateFunctionBox( 'Number', 'sqrt(a)' )
    C2_div1 = constraint.CreateFunctionBox( 'Number', 'Divide (a/b)' )
    C2_M02sM21 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C2_M20sM02 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C2_M01sM10 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C2_W = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C2_X = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C2_Y = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C2_Z = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C2_toEuler = constraint.CreateFunctionBox( 'My Macros', '#toEulerAngle' )
    
    constraint.SetBoxPosition( C2_M00pM11, 170, 450 )
    constraint.SetBoxPosition( C2_M00pM11pM22, 430, 450 )
    constraint.SetBoxPosition( C2_M00pM11pM22p1, 690, 450 )
    constraint.SetBoxPosition( C2_sqrt, 950, 450 )
    constraint.SetBoxPosition( C2_div1, 950, 500) 
    constraint.SetBoxPosition( C2_M02sM21, 950, 570 )
    constraint.SetBoxPosition( C2_M20sM02, 950, 640 )
    constraint.SetBoxPosition( C2_M01sM10, 950, 710 )
    constraint.SetBoxPosition( C2_W, 1250, 460 )
    constraint.SetBoxPosition( C2_X, 1250, 530 )
    constraint.SetBoxPosition( C2_Y, 1250, 600 )
    constraint.SetBoxPosition( C2_Z, 1250, 670 )
    constraint.SetBoxPosition( C2_toEuler, 1550, 550 )
    
    C2_M00pM11.Name = 'Case2 (M0.X + M1.Y)'
    C2_M00pM11pM22.Name = 'Case2 (+ M2.Z)'
    C2_M00pM11pM22p1.Name = 'Case2 (+ 1)'
    C2_sqrt.Name = 'Case2 Sqrt()'
    C2_div1.Name = 'Case2 (a/b)'
    C2_M02sM21.Name = 'Case2 (M0.Z - M2.Y)'
    C2_M20sM02.Name = 'Case2 (M2.X - M0.Z)'
    C2_M01sM10.Name = 'Case2 (M0.Y - M1.X)'
    C2_W.Name = 'Case2 (x) W'
    C2_X.Name = 'Case2 (x) X'
    C2_Y.Name = 'Case2 (x) Y'
    C2_Z.Name = 'Case2 (x) Z'
    C2_toEuler.Name = 'Case2 Quaternion to Euler'
    
    C2_M00pM11A = FindAnimationNode( C2_M00pM11.AnimationNodeInGet(), "a")
    C2_M00pM11B = FindAnimationNode( C2_M00pM11.AnimationNodeInGet(), "b")
    C2_M00pM11Out = FindAnimationNode( C2_M00pM11.AnimationNodeOutGet(), "Result")
    C2_M00pM11pM22A = FindAnimationNode( C2_M00pM11pM22.AnimationNodeInGet(), "a")
    C2_M00pM11pM22B = FindAnimationNode( C2_M00pM11pM22.AnimationNodeInGet(), "b")
    C2_M00pM11pM22Out = FindAnimationNode( C2_M00pM11pM22.AnimationNodeOutGet(), "Result")
    C2_M00pM11pM22p1A = FindAnimationNode( C2_M00pM11pM22p1.AnimationNodeInGet(), "a")
    C2_M00pM11pM22p1B = FindAnimationNode( C2_M00pM11pM22p1.AnimationNodeInGet(), "b")
    C2_M00pM11pM22p1Out = FindAnimationNode( C2_M00pM11pM22p1.AnimationNodeOutGet(), "Result")
    C2_sqrtIn = FindAnimationNode( C2_sqrt.AnimationNodeInGet(), "a")
    C2_sqrtOut = FindAnimationNode( C2_sqrt.AnimationNodeOutGet(), "Result")
    C2_div1A = FindAnimationNode( C2_div1.AnimationNodeInGet(), "a")
    C2_div1B = FindAnimationNode( C2_div1.AnimationNodeInGet(), "b")
    C2_div1Out = FindAnimationNode( C2_div1.AnimationNodeOutGet(), "Result")
    C2_M02sM21A = FindAnimationNode( C2_M02sM21.AnimationNodeInGet(), "a")
    C2_M02sM21B = FindAnimationNode( C2_M02sM21.AnimationNodeInGet(), "b")
    C2_M02sM21Out = FindAnimationNode( C2_M02sM21.AnimationNodeOutGet(), "Result")
    C2_M20sM02A = FindAnimationNode( C2_M20sM02.AnimationNodeInGet(), "a")
    C2_M20sM02B = FindAnimationNode( C2_M20sM02.AnimationNodeInGet(), "b")
    C2_M20sM02Out = FindAnimationNode( C2_M20sM02.AnimationNodeOutGet(), "Result")
    C2_M01sM10A = FindAnimationNode( C2_M01sM10.AnimationNodeInGet(), "a")
    C2_M01sM10B = FindAnimationNode( C2_M01sM10.AnimationNodeInGet(), "b")
    C2_M01sM10Out = FindAnimationNode( C2_M01sM10.AnimationNodeOutGet(), "Result")
    C2_WA = FindAnimationNode( C2_W.AnimationNodeInGet(), "a")
    C2_WB = FindAnimationNode( C2_W.AnimationNodeInGet(), "b")
    C2_WOut = FindAnimationNode( C2_W.AnimationNodeOutGet(), "Result")
    C2_XA = FindAnimationNode( C2_X.AnimationNodeInGet(), "a")
    C2_XB = FindAnimationNode( C2_X.AnimationNodeInGet(), "b")
    C2_XOut = FindAnimationNode( C2_X.AnimationNodeOutGet(), "Result")
    C2_YA = FindAnimationNode( C2_Y.AnimationNodeInGet(), "a")
    C2_YB = FindAnimationNode( C2_Y.AnimationNodeInGet(), "b")
    C2_YOut = FindAnimationNode( C2_Y.AnimationNodeOutGet(), "Result")
    C2_ZA = FindAnimationNode( C2_Z.AnimationNodeInGet(), "a")
    C2_ZB = FindAnimationNode( C2_Z.AnimationNodeInGet(), "b")
    C2_ZOut = FindAnimationNode( C2_Z.AnimationNodeOutGet(), "Result")
    C2_toEulerW = FindAnimationNode( C2_toEuler.AnimationNodeInGet(), "MacroInput0")
    C2_toEulerX = FindAnimationNode( C2_toEuler.AnimationNodeInGet(), "MacroInput1")
    C2_toEulerY = FindAnimationNode( C2_toEuler.AnimationNodeInGet(), "MacroInput2")
    C2_toEulerZ = FindAnimationNode( C2_toEuler.AnimationNodeInGet(), "MacroInput3")
    C2_toEulerOut = FindAnimationNode( C2_toEuler.AnimationNodeOutGet(), "MacroOutput0")
    
    FBConnect( M0X, C2_M00pM11A )
    FBConnect( M1Y, C2_M00pM11B )
    FBConnect( C2_M00pM11Out, C2_M00pM11pM22A )
    FBConnect( M2Z, C2_M00pM11pM22B )
    FBConnect( C2_M00pM11pM22Out, C2_M00pM11pM22p1A )
    C2_M00pM11pM22p1B.WriteData( [1.0] )
    FBConnect( C2_M00pM11pM22p1Out, C2_sqrtIn )
    
    C2_div1A.WriteData( [0.5] )
    FBConnect( C2_sqrtOut, C2_div1B )
    FBConnect( M0Z, C2_M02sM21A )
    FBConnect( M2Y, C2_M02sM21B )
    FBConnect( M2X, C2_M20sM02A )
    FBConnect( M0Z, C2_M20sM02B )
    FBConnect( M0Y, C2_M01sM10A )
    FBConnect( M1X, C2_M01sM10B )
    FBConnect( C2_sqrtOut, C2_WA )
    C2_WB.WriteData( [0.5] )
    FBConnect( C2_M02sM21Out, C2_XA )
    FBConnect( C2_div1Out, C2_XB )
    FBConnect( C2_M20sM02Out, C2_YA )
    FBConnect( C2_div1Out, C2_YB )
    FBConnect( C2_M01sM10Out, C2_ZA )
    FBConnect( C2_div1Out, C2_ZB )
    FBConnect( C2_WOut, C2_toEulerW )
    FBConnect( C2_XOut, C2_toEulerX )
    FBConnect( C2_YOut, C2_toEulerY )
    FBConnect( C2_ZOut, C2_toEulerZ )
    
    #############################
    # Evaluate Quaternion Case3 #
    #############################    
    C3_1pM11 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C3_1pM11sM00 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C3_1pM11sM00sM22 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    
    C3_M12sM21 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C3_sqrt = constraint.CreateFunctionBox( 'Number', 'sqrt(a)' )
    C3_div1 = constraint.CreateFunctionBox( 'Number', 'Divide (a/b)' )
    C3_M01pM10 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C3_M02pM20 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C3_W = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C3_X = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C3_Y = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C3_Z = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C3_toEuler = constraint.CreateFunctionBox( 'My Macros', '#toEulerAngle' )
    
    constraint.SetBoxPosition( C3_1pM11, 170, 1060 )
    constraint.SetBoxPosition( C3_1pM11sM00, 430, 860 )
    constraint.SetBoxPosition( C3_1pM11sM00sM22, 690, 860 )
    
    constraint.SetBoxPosition( C3_M12sM21, 950, 800 )
    constraint.SetBoxPosition( C3_sqrt, 950, 870) 
    constraint.SetBoxPosition( C3_div1, 950, 910 )
    constraint.SetBoxPosition( C3_M01pM10, 950, 980 )
    constraint.SetBoxPosition( C3_M02pM20, 950, 1050 )
    constraint.SetBoxPosition( C3_W, 1250, 820 )
    constraint.SetBoxPosition( C3_X, 1250, 890 )
    constraint.SetBoxPosition( C3_Y, 1250, 960 )
    constraint.SetBoxPosition( C3_Z, 1250, 1030 )
    constraint.SetBoxPosition( C3_toEuler, 1550, 900 )
    
    C3_1pM11.Name = 'Case 3 and 4 (1 + M1.Y)'
    C3_1pM11sM00.Name = 'Case3 (- M0.X)'
    C3_1pM11sM00sM22.Name = 'Case3 (- M2.Z)'
    C3_M12sM21.Name = 'Case3 (M1.Z - M2.Y)'
    C3_sqrt.Name = 'Case3 Sqrt()'
    C3_div1.Name = 'Case3 (a/b)'
    C3_M01pM10.Name = 'Case3 (M0.Y + M1.X)'
    C3_M02pM20.Name = 'Case3 (M0.Z + M2.X)'
    C3_W.Name = 'Case3 (x) W'
    C3_X.Name = 'Case3 (x) X'
    C3_Y.Name = 'Case3 (x) Y'
    C3_Z.Name = 'Case3 (x) Z'
    C3_toEuler.Name = 'Case3 Quaternion to Euler'
    
    C3_1pM11A = FindAnimationNode( C3_1pM11.AnimationNodeInGet(), "a")
    C3_1pM11B = FindAnimationNode( C3_1pM11.AnimationNodeInGet(), "b")
    C3_1pM11Out = FindAnimationNode( C3_1pM11.AnimationNodeOutGet(), "Result")
    C3_1pM11sM00A = FindAnimationNode( C3_1pM11sM00.AnimationNodeInGet(), "a")
    C3_1pM11sM00B = FindAnimationNode( C3_1pM11sM00.AnimationNodeInGet(), "b")
    C3_1pM11sM00Out = FindAnimationNode( C3_1pM11sM00.AnimationNodeOutGet(), "Result")
    C3_1pM11sM00sM22A = FindAnimationNode( C3_1pM11sM00sM22.AnimationNodeInGet(), "a")
    C3_1pM11sM00sM22B = FindAnimationNode( C3_1pM11sM00sM22.AnimationNodeInGet(), "b")
    C3_1pM11sM00sM22Out = FindAnimationNode( C3_1pM11sM00sM22.AnimationNodeOutGet(), "Result")    
    
    C3_M12sM21A = FindAnimationNode( C3_M12sM21.AnimationNodeInGet(), "a")
    C3_M12sM21B = FindAnimationNode( C3_M12sM21.AnimationNodeInGet(), "b")
    C3_M12sM21Out = FindAnimationNode( C3_M12sM21.AnimationNodeOutGet(), "Result")
    C3_sqrtIn = FindAnimationNode( C3_sqrt.AnimationNodeInGet(), "a")
    C3_sqrtOut = FindAnimationNode( C3_sqrt.AnimationNodeOutGet(), "Result")
    C3_div1A = FindAnimationNode( C3_div1.AnimationNodeInGet(), "a")
    C3_div1B = FindAnimationNode( C3_div1.AnimationNodeInGet(), "b")
    C3_div1Out = FindAnimationNode( C3_div1.AnimationNodeOutGet(), "Result")
    C3_M01pM10A = FindAnimationNode( C3_M01pM10.AnimationNodeInGet(), "a")
    C3_M01pM10B = FindAnimationNode( C3_M01pM10.AnimationNodeInGet(), "b")
    C3_M01pM10Out = FindAnimationNode( C3_M01pM10.AnimationNodeOutGet(), "Result")
    C3_M02pM20A = FindAnimationNode( C3_M02pM20.AnimationNodeInGet(), "a")
    C3_M02pM20B = FindAnimationNode( C3_M02pM20.AnimationNodeInGet(), "b")
    C3_M02pM20Out = FindAnimationNode( C3_M02pM20.AnimationNodeOutGet(), "Result")
    C3_WA = FindAnimationNode( C3_W.AnimationNodeInGet(), "a")
    C3_WB = FindAnimationNode( C3_W.AnimationNodeInGet(), "b")
    C3_WOut = FindAnimationNode( C3_W.AnimationNodeOutGet(), "Result")
    C3_XA = FindAnimationNode( C3_X.AnimationNodeInGet(), "a")
    C3_XB = FindAnimationNode( C3_X.AnimationNodeInGet(), "b")
    C3_XOut = FindAnimationNode( C3_X.AnimationNodeOutGet(), "Result")
    C3_YA = FindAnimationNode( C3_Y.AnimationNodeInGet(), "a")
    C3_YB = FindAnimationNode( C3_Y.AnimationNodeInGet(), "b")
    C3_YOut = FindAnimationNode( C3_Y.AnimationNodeOutGet(), "Result")
    C3_ZA = FindAnimationNode( C3_Z.AnimationNodeInGet(), "a")
    C3_ZB = FindAnimationNode( C3_Z.AnimationNodeInGet(), "b")
    C3_ZOut = FindAnimationNode( C3_Z.AnimationNodeOutGet(), "Result")
    C3_toEulerW = FindAnimationNode( C3_toEuler.AnimationNodeInGet(), "MacroInput0")
    C3_toEulerX = FindAnimationNode( C3_toEuler.AnimationNodeInGet(), "MacroInput1")
    C3_toEulerY = FindAnimationNode( C3_toEuler.AnimationNodeInGet(), "MacroInput2")
    C3_toEulerZ = FindAnimationNode( C3_toEuler.AnimationNodeInGet(), "MacroInput3")
    C3_toEulerOut = FindAnimationNode( C3_toEuler.AnimationNodeOutGet(), "MacroOutput0")
    
    C3_1pM11A.WriteData( [1.0] )
    FBConnect( M1Y, C3_1pM11B )
    FBConnect( C3_1pM11Out, C3_1pM11sM00A )
    FBConnect( M0X, C3_1pM11sM00B )
    FBConnect( C3_1pM11sM00Out, C3_1pM11sM00sM22A )
    FBConnect( M2Z, C3_1pM11sM00sM22B )
    FBConnect( C3_1pM11sM00sM22Out, C3_sqrtIn )
    
    FBConnect( M1Z, C3_M12sM21A )
    FBConnect( M2Y, C3_M12sM21B )
    C3_div1A.WriteData( [0.5] )
    FBConnect( C3_sqrtOut, C3_div1B )
    FBConnect( M0Y, C3_M01pM10A )
    FBConnect( M1X, C3_M01pM10B )
    FBConnect( M0Z, C3_M02pM20A )
    FBConnect( M2X, C3_M02pM20B )
    FBConnect( C3_M12sM21Out, C3_WA )
    FBConnect( C3_div1Out, C3_WB )
    C3_XA.WriteData( [0.5] )
    FBConnect( C3_sqrtOut, C3_XB )
    FBConnect( C3_M01pM10Out, C3_YA )
    FBConnect( C3_div1Out, C3_YB )
    FBConnect( C3_M02pM20Out, C3_ZA )
    FBConnect( C3_div1Out, C3_ZB )
    FBConnect( C3_WOut, C3_toEulerW )
    FBConnect( C3_XOut, C3_toEulerX )
    FBConnect( C3_YOut, C3_toEulerY )
    FBConnect( C3_ZOut, C3_toEulerZ )
    
    #############################
    # Evaluate Quaternion Case4 #
    #############################
    C4_1pM11sM00 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    C4_1pM11sM00sM22 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )
    
    C4_M20sM02 = constraint.CreateFunctionBox( 'Number', 'Subtract (a - b)' )    
    C4_M10pM01 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C4_sqrt = constraint.CreateFunctionBox( 'Number', 'sqrt(a)' )
    C4_div1 = constraint.CreateFunctionBox( 'Number', 'Divide (a/b)' )
    C4_M21pM12 = constraint.CreateFunctionBox( 'Number', 'Add (a + b)' )
    C4_W = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C4_X = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C4_Y = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C4_Z = constraint.CreateFunctionBox( 'Number', 'Multiply (a x b)' )
    C4_toEuler = constraint.CreateFunctionBox( 'My Macros', '#toEulerAngle' )
    
    constraint.SetBoxPosition( C4_1pM11sM00, 430, 1280 )
    constraint.SetBoxPosition( C4_1pM11sM00sM22, 690, 1280 )
    
    constraint.SetBoxPosition( C4_M20sM02, 950, 1140 )
    constraint.SetBoxPosition( C4_M10pM01, 950, 1210) 
    constraint.SetBoxPosition( C4_sqrt, 950, 1280 )
    constraint.SetBoxPosition( C4_div1, 950, 1320 )
    constraint.SetBoxPosition( C4_M21pM12, 950, 1390 )
    constraint.SetBoxPosition( C4_W, 1250, 1170 )
    constraint.SetBoxPosition( C4_X, 1250, 1240 )
    constraint.SetBoxPosition( C4_Y, 1250, 1310 )
    constraint.SetBoxPosition( C4_Z, 1250, 1380 )
    constraint.SetBoxPosition( C4_toEuler, 1550, 1250 )
    
    C4_1pM11sM00.Name = 'Case4 (- M0.X)'
    C4_1pM11sM00sM22.Name = 'Case4 (- M2.Z'
    C4_M20sM02.Name = 'Case4 (M2.X - M0.Z)'
    C4_M10pM01.Name = 'Case4 (M0.Y + M1.X)'
    C4_sqrt.Name = 'Case4 Sqrt()'
    C4_div1.Name = 'Case4 (a/b)'    
    C4_M21pM12.Name = 'Case4 (M2.Y + M1.Z)'
    C4_W.Name = 'Case4 (x) W'
    C4_X.Name = 'Case4 (x) X'
    C4_Y.Name = 'Case4 (x) Y'
    C4_Z.Name = 'Case4 (x) Z'
    C4_toEuler.Name = 'Case4 Quaternion to Euler'
    
    C4_1pM11sM00A = FindAnimationNode( C4_1pM11sM00.AnimationNodeInGet(), "a")
    C4_1pM11sM00B = FindAnimationNode( C4_1pM11sM00.AnimationNodeInGet(), "b")
    C4_1pM11sM00Out = FindAnimationNode( C4_1pM11sM00.AnimationNodeOutGet(), "Result")
    C4_1pM11sM00sM22A = FindAnimationNode( C4_1pM11sM00sM22.AnimationNodeInGet(), "a")
    C4_1pM11sM00sM22B = FindAnimationNode( C4_1pM11sM00sM22.AnimationNodeInGet(), "b")
    C4_1pM11sM00sM22Out = FindAnimationNode( C4_1pM11sM00sM22.AnimationNodeOutGet(), "Result")
    
    C4_M20sM02A = FindAnimationNode( C4_M20sM02.AnimationNodeInGet(), "a")
    C4_M20sM02B = FindAnimationNode( C4_M20sM02.AnimationNodeInGet(), "b")
    C4_M20sM02Out = FindAnimationNode( C4_M20sM02.AnimationNodeOutGet(), "Result")
    C4_M10pM01A = FindAnimationNode( C4_M10pM01.AnimationNodeInGet(), "a")
    C4_M10pM01B = FindAnimationNode( C4_M10pM01.AnimationNodeInGet(), "b")
    C4_M10pM01Out = FindAnimationNode( C4_M10pM01.AnimationNodeOutGet(), "Result")
    C4_sqrtIn = FindAnimationNode( C4_sqrt.AnimationNodeInGet(), "a")
    C4_sqrtOut = FindAnimationNode( C4_sqrt.AnimationNodeOutGet(), "Result")
    C4_div1A = FindAnimationNode( C4_div1.AnimationNodeInGet(), "a")
    C4_div1B = FindAnimationNode( C4_div1.AnimationNodeInGet(), "b")
    C4_div1Out = FindAnimationNode( C4_div1.AnimationNodeOutGet(), "Result")    
    C4_M21pM12A = FindAnimationNode( C4_M21pM12.AnimationNodeInGet(), "a")
    C4_M21pM12B = FindAnimationNode( C4_M21pM12.AnimationNodeInGet(), "b")
    C4_M21pM12Out = FindAnimationNode( C4_M21pM12.AnimationNodeOutGet(), "Result")
    C4_WA = FindAnimationNode( C4_W.AnimationNodeInGet(), "a")
    C4_WB = FindAnimationNode( C4_W.AnimationNodeInGet(), "b")
    C4_WOut = FindAnimationNode( C4_W.AnimationNodeOutGet(), "Result")
    C4_XA = FindAnimationNode( C4_X.AnimationNodeInGet(), "a")
    C4_XB = FindAnimationNode( C4_X.AnimationNodeInGet(), "b")
    C4_XOut = FindAnimationNode( C4_X.AnimationNodeOutGet(), "Result")
    C4_YA = FindAnimationNode( C4_Y.AnimationNodeInGet(), "a")
    C4_YB = FindAnimationNode( C4_Y.AnimationNodeInGet(), "b")
    C4_YOut = FindAnimationNode( C4_Y.AnimationNodeOutGet(), "Result")
    C4_ZA = FindAnimationNode( C4_Z.AnimationNodeInGet(), "a")
    C4_ZB = FindAnimationNode( C4_Z.AnimationNodeInGet(), "b")
    C4_ZOut = FindAnimationNode( C4_Z.AnimationNodeOutGet(), "Result")
    C4_toEulerW = FindAnimationNode( C4_toEuler.AnimationNodeInGet(), "MacroInput0")
    C4_toEulerX = FindAnimationNode( C4_toEuler.AnimationNodeInGet(), "MacroInput1")
    C4_toEulerY = FindAnimationNode( C4_toEuler.AnimationNodeInGet(), "MacroInput2")
    C4_toEulerZ = FindAnimationNode( C4_toEuler.AnimationNodeInGet(), "MacroInput3")
    C4_toEulerOut = FindAnimationNode( C4_toEuler.AnimationNodeOutGet(), "MacroOutput0")
    
    FBConnect( C3_1pM11Out, C4_1pM11sM00A )
    FBConnect( M0X, C4_1pM11sM00B )
    FBConnect( C4_1pM11sM00Out, C4_1pM11sM00sM22A )
    FBConnect( M2Z, C4_1pM11sM00sM22B )
    FBConnect( C4_1pM11sM00sM22Out, C4_sqrtIn )    
    FBConnect( M2X, C4_M20sM02A )
    FBConnect( M0Z, C4_M20sM02B )
    FBConnect( M1X, C4_M10pM01A )
    FBConnect( M0Y, C4_M10pM01B )
    FBConnect( C4_sqrtOut, C4_div1B )
    C4_div1A.WriteData( [0.5] )
    FBConnect( M2Y, C4_M21pM12A )
    FBConnect( M1Z, C4_M21pM12B )    
    FBConnect( C4_M20sM02Out, C4_WA )
    FBConnect( C4_div1Out, C4_WB )
    FBConnect( C4_M10pM01Out, C4_XA )
    FBConnect( C4_div1Out, C4_XB )
    C4_YA.WriteData( [0.5] )
    FBConnect( C4_sqrtOut, C4_YB )
    FBConnect( C4_M21pM12Out, C4_ZA )
    FBConnect( C4_div1Out, C4_ZB )
    FBConnect( C4_WOut, C4_toEulerW )
    FBConnect( C4_XOut, C4_toEulerX )
    FBConnect( C4_YOut, C4_toEulerY )
    FBConnect( C4_ZOut, C4_toEulerZ )
    
    #Conditions and wrap up
    IfCase2 = constraint.CreateFunctionBox( 'Vector', 'IF Cond Then A Else B' )
    IfCase3 = constraint.CreateFunctionBox( 'Vector', 'IF Cond Then A Else B' )
    IfCase4 = constraint.CreateFunctionBox( 'Vector', 'IF Cond Then A Else B' )
    C2_isGreater = constraint.CreateFunctionBox( 'Number', 'Is Greater (a > b)' )
    C3_isGreatEqualA = constraint.CreateFunctionBox( 'Number', 'Is Greater or Equal (a >= b)' )
    C3_isGreatEqualB = constraint.CreateFunctionBox( 'Number', 'Is Greater or Equal (a >= b)' )
    C3_AND = constraint.CreateFunctionBox( 'Boolean', 'AND' )
    C4_isGreater = constraint.CreateFunctionBox( 'Number', 'Is Greater (a > b)' )
    Final_AimOffset = constraint.CreateFunctionBox( 'Rotation', 'Add (R1 + R2)' )
    Final_Output = constraint.CreateFunctionBox( 'Macro Tools', 'Macro Output Vector' )
    
    IfCase2.Name = 'Case 2'
    IfCase3.Name = 'Case 3'
    IfCase4.Name = 'Case 4'
    C2_isGreater.Name = 'Case2 (a > b)'
    C3_isGreatEqualA.Name = 'Case3a (a >= b)'
    C3_isGreatEqualB.Name = 'Case3b (a >= b)'
    C3_AND.Name = 'Case3 AND'
    C4_isGreater.Name = 'Case4 (a > b)'
    Final_AimOffset.Name = 'Rotation Offset'
    Final_Output.Name = 'LookAt'
    
    constraint.SetBoxPosition( IfCase2, 2200, 200 )
    constraint.SetBoxPosition( IfCase3, 2220, 300 )
    constraint.SetBoxPosition( IfCase4, 2240, 400 )
    constraint.SetBoxPosition( C2_isGreater, 1650, 200 )
    constraint.SetBoxPosition( C3_isGreatEqualA, 1580, 275 )
    constraint.SetBoxPosition( C3_isGreatEqualB, 1580, 350 )
    constraint.SetBoxPosition( C3_AND, 1830, 300 )
    constraint.SetBoxPosition( C4_isGreater, 1650, 425 )
    constraint.SetBoxPosition( Final_AimOffset, 2500, 425 )
    constraint.SetBoxPosition( Final_Output, 2750, 425 )
    
    C2_isGreaterA = FindAnimationNode( C2_isGreater.AnimationNodeInGet(), "a")
    C2_isGreaterB = FindAnimationNode( C2_isGreater.AnimationNodeInGet(), "b")
    C2_isGreaterOut = FindAnimationNode( C2_isGreater.AnimationNodeOutGet(), "Result")
    C3_isGreatEqualAA = FindAnimationNode( C3_isGreatEqualA.AnimationNodeInGet(), "a")
    C3_isGreatEqualAB = FindAnimationNode( C3_isGreatEqualA.AnimationNodeInGet(), "b")
    C3_isGreatEqualAOut = FindAnimationNode( C3_isGreatEqualA.AnimationNodeOutGet(), "Result")
    C3_isGreatEqualBA = FindAnimationNode( C3_isGreatEqualB.AnimationNodeInGet(), "a")
    C3_isGreatEqualBB = FindAnimationNode( C3_isGreatEqualB.AnimationNodeInGet(), "b")
    C3_isGreatEqualBOut = FindAnimationNode( C3_isGreatEqualB.AnimationNodeOutGet(), "Result")
    C3_ANDA = FindAnimationNode( C3_AND.AnimationNodeInGet(), "a")
    C3_ANDB = FindAnimationNode( C3_AND.AnimationNodeInGet(), "b")
    C3_ANDOut = FindAnimationNode( C3_AND.AnimationNodeOutGet(), "Result")
    C4_isGreaterA = FindAnimationNode( C4_isGreater.AnimationNodeInGet(), "a")
    C4_isGreaterB = FindAnimationNode( C4_isGreater.AnimationNodeInGet(), "b")
    C4_isGreaterOut = FindAnimationNode( C4_isGreater.AnimationNodeOutGet(), "Result")
    
    IfCase2A = FindAnimationNode( IfCase2.AnimationNodeInGet(), "a")
    IfCase2B = FindAnimationNode( IfCase2.AnimationNodeInGet(), "b")
    IfCase2C = FindAnimationNode( IfCase2.AnimationNodeInGet(), "Cond")
    IfCase2Out = FindAnimationNode( IfCase2.AnimationNodeOutGet(), "Result")
    IfCase3A = FindAnimationNode( IfCase3.AnimationNodeInGet(), "a")
    IfCase3B = FindAnimationNode( IfCase3.AnimationNodeInGet(), "b")
    IfCase3C = FindAnimationNode( IfCase3.AnimationNodeInGet(), "Cond")
    IfCase3Out = FindAnimationNode( IfCase3.AnimationNodeOutGet(), "Result")
    IfCase4A = FindAnimationNode( IfCase4.AnimationNodeInGet(), "a")
    IfCase4B = FindAnimationNode( IfCase4.AnimationNodeInGet(), "b")
    IfCase4C = FindAnimationNode( IfCase4.AnimationNodeInGet(), "Cond")
    IfCase4Out = FindAnimationNode( IfCase4.AnimationNodeOutGet(), "Result")
    Final_AimOffsetA = FindAnimationNode( Final_AimOffset.AnimationNodeInGet(), "Ra")
    Final_AimOffsetB = FindAnimationNode( Final_AimOffset.AnimationNodeInGet(), "Rb")
    Final_AimOffsetOut = FindAnimationNode( Final_AimOffset.AnimationNodeOutGet(), "Result")
    Final_OutputOut = FindAnimationNode( Final_Output.AnimationNodeInGet(), "Output")
    
    FBConnect( C2_M00pM11pM22Out, C2_isGreaterA )
    C2_isGreaterB.WriteData( [0.0] )    
    FBConnect( C2_isGreaterOut, IfCase2C )
    FBConnect( M0X, C3_isGreatEqualAA )
    FBConnect( M1Y, C3_isGreatEqualAB )
    FBConnect( M0X, C3_isGreatEqualBA )
    FBConnect( M2Z, C3_isGreatEqualBB )
    FBConnect( C3_isGreatEqualAOut, C3_ANDA )
    FBConnect( C3_isGreatEqualBOut, C3_ANDB )
    FBConnect( C3_ANDOut, IfCase3C )
    FBConnect( M1Y, C4_isGreaterA )
    FBConnect( M2Z, C4_isGreaterB )
    FBConnect( C4_isGreaterOut, IfCase4C )
    
    FBConnect( C2_toEulerOut, IfCase2A )
    FBConnect( C1_toEulerOut, IfCase2B )
    FBConnect( IfCase2Out, IfCase3B )
    FBConnect( C3_toEulerOut, IfCase3A )
    FBConnect( IfCase3Out, IfCase4B )
    FBConnect( C4_toEulerOut, IfCase4A )
    FBConnect( IfCase4Out, Final_AimOffsetA )
    FBConnect( macInAimOut, Final_AimOffsetB )
    FBConnect( Final_AimOffsetOut, Final_OutputOut )

    
toEulerAngle()
lookAtMacro()