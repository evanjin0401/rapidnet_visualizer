'''
Created on Jul 1, 2009

@author: shivkumar
'''

from ns3.model.net_world_node import NetWorldNode
from ns3.model.net_world_model import NetWorldModel
from ns3.viewer.node_style import NodeShape, NodeStyle
from ns3.viewer.link_style import LinkStyle
from ns3.viewer.animation_model import AnimationModel
from ns3.viewer.time_slider import TimeSlider
from ns3.viewer.net_view_area import NetViewArea

node = NetWorldNode (7)
print node.id

model = NetWorldModel ()
print model.events

nodeStyle = NodeStyle(hasLineWidth = True)
print nodeStyle.hasLineWidth, nodeStyle.double, nodeStyle.lineWidth

linkStyle = LinkStyle(lw = 5, a = 9)
print linkStyle.r, linkStyle.a

anim = AnimationModel ()
anim.SetWorldModel (model)
anim.Start ()
anim.Stop ()

timeSlider = TimeSlider()
timeSlider.SetWorldModel(model)
timeSlider.SetAnimationTime(10)

netViewArea = NetViewArea ()
