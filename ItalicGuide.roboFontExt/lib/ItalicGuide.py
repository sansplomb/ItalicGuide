from mojo.events import addObserver, removeObserver
from AppKit import *
import math
from mojo.extensions import getExtensionDefault, setExtensionDefault
from robofab.world import *

defaultKeyStub = "com.sansplomb.italicGuide."
defaultKeyObserverVisibility = defaultKeyStub + "displayGuide"

gridColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0, 0.5)

def getItalAngle(f):
	italAngle = f.info.italicAngle
	if italAngle == None:
		italAngle = 0
	return italAngle

def getItalRatio(italAngle):
    italRatio = math.tan(math.radians(-italAngle))
    return italRatio

def getxShift(yShift, italRatio):
	xShift = yShift * italRatio
	return xShift
	
def toggleObserverVisibility():	
    state = not getExtensionDefault(defaultKeyObserverVisibility)
    setExtensionDefault(defaultKeyObserverVisibility, state)
    
class italicGuide():
    def __init__(self, f):
        addObserver(self, "mouseDown", "mouseDown")
        addObserver(self, "mouseUp", "mouseUp")
        #addObserver(self, "fontWillClose", "fontWillClose")
        #addObserver(self, "fontDidOpen", "fontDidOpen")
        self.f = f
        self.italAngle = None

    def fontDidOpen(self, font):
        if self.f == None:
            addObserver(self, "mouseDown", "mouseDown")
            addObserver(self, "mouseUp", "mouseUp")
            addObserver(self, "fontWillClose", "fontWillClose")
            self.f = font

    def mouseDown(self, info):
        self.f = CurrentFont()
        self.x = info["point"].x
        self.y = info["point"].y
        self.italAngle = getItalAngle(self.f)
        addObserver(self, "draw", "draw")
        addObserver(self, "mouseDragged", "mouseDragged")
        if getExtensionDefault(defaultKeyObserverVisibility) == False:
            removeObserver(self, "mouseDragged")
            removeObserver(self, "draw")
        
    def mouseUp(self, info):
        removeObserver(self, "draw")
        
    def mouseDragged(self, info):
        self.x = info["point"].x
        self.y = info["point"].y
        
    def fontWillClose(self, font):
        #print font
        removeObserver(self, "mouseDown")
        removeObserver(self, "mouseUp")
        removeObserver(self, "mouseDragged")
        removeObserver(self, "fontWillClose")
        
        
    def draw(self, info):
        self.g = CurrentGlyph()
        if self.g == None:
            return
        scale = info['scale']
        width = self.g.width
        path = NSBezierPath.bezierPath()
        path.moveToPoint_((self.x, self.y))
        path.lineToPoint_((self.x + getxShift(2.0*self.f.info.unitsPerEm, getItalRatio(self.italAngle)), self.y+2.0*self.f.info.unitsPerEm))
        path.moveToPoint_((self.x, self.y))
        path.lineToPoint_((self.x + getxShift(-2.0*self.f.info.unitsPerEm, getItalRatio(self.italAngle)), self.y-2.0*self.f.info.unitsPerEm))
        gridColor.set()
        path.setLineWidth_(scale)
        path.stroke()
        