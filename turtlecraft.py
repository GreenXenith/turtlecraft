"""
This was made mostly as a joke to say "yes I can do that".

NOTE:
Tkinter stores each drawn path as an object. Because each pixel has 4 sides and each face has 256 pixels, a face is made of 1024 objects.
With ~100 visible faces, there are more than 100k objects being stored by Tkinter. This causes some serious performance hits (slow render speed).
Could be solved by drawing directly to the canvas (if possible).
"""

"""
MIT Copyright 2020 GreenXenith

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import turtle
import colorsys # Used for face shading

### Turtle initialization
screen = turtle.Screen()
screen.colormode(255)
screen.tracer(0, 0) # This speeds up draw time (a lot)
screen.bgcolor([134, 199, 248])
screen.title("TurtleCraft")

cursor = turtle.Turtle()
cursor.setundobuffer(None) # At least _try_ to conserve memory
cursor.speed(0)
cursor.penup()

cursor.hideturtle()

### Constants
PIXEL = 2 # Turtle pixels per Minecraft pixel
METER = PIXEL * 16

### Helper functions
# Convert grid coordinates to screen coordinates
def isoToScreen(x, y, z):
	screenX = (x - z) * (METER - PIXEL * 2) # I dont know why this works, it just does
	screenY = -(x + z - (y * 2)) * METER / 2
	return screenX, screenY

# Change brightness of a color
def value(rgb, v):
	HSV = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
	RGB = colorsys.hsv_to_rgb(HSV[0], HSV[1], max(0, min(HSV[2] + v, 1)))
	return (round(RGB[0] * 255), round(RGB[1] * 255), round(RGB[2] * 255))

### Game data
# Texture definitions (Flat RGB arrays generated via Lua script. I suggest readers disable line wrapping for their editor/IDE)
# Stolen from Minetest's minetest_game "default" mod (https://github.com/minetest/minetest_game/blob/5.3.0/mods/default/textures/)
# Licenses (CC-BY-SA 3.0):
#   dirt: random-geek
#   grass: TumeniNodes
#   stone: Cisoun
#   wood: BlockMen
textures = {
	"dirt": [[[112,82,56],[106,75,49],[90,62,38],[93,63,38],[108,78,53],[112,82,56],[90,62,38],[112,82,56],[100,69,42],[84,52,22],[93,63,38],[108,78,53],[104,84,70],[93,63,38],[106,75,49],[108,78,53],],[[90,62,38],[88,55,26],[100,69,42],[100,69,42],[108,78,53],[90,62,38],[90,62,38],[90,62,38],[95,66,42],[108,78,53],[112,82,56],[88,55,26],[95,66,42],[95,66,42],[93,63,38],[112,82,56],],[[89,58,32],[124,92,65],[102,73,48],[95,66,42],[88,55,26],[108,78,53],[95,66,42],[88,55,26],[108,78,53],[124,92,65],[93,63,38],[88,55,26],[95,66,42],[70,40,10],[86,55,27],[95,66,42],],[[89,58,32],[89,58,32],[84,52,22],[90,62,38],[89,58,32],[93,63,38],[95,66,42],[93,63,38],[95,66,42],[106,75,49],[106,75,49],[95,66,42],[102,73,48],[112,82,56],[93,63,38],[86,55,27],],[[93,63,38],[84,52,22],[93,63,38],[102,73,48],[70,40,10],[95,66,42],[108,78,53],[102,73,48],[95,66,42],[93,63,38],[112,82,56],[88,55,26],[102,73,48],[108,78,53],[95,66,42],[95,66,42],],[[100,69,42],[90,62,38],[131,106,88],[95,66,42],[100,69,42],[112,82,56],[106,75,49],[102,73,48],[88,55,26],[95,66,42],[90,62,38],[95,66,42],[93,63,38],[95,66,42],[70,40,10],[112,82,56],],[[95,66,42],[104,84,70],[102,73,48],[100,69,42],[88,55,26],[95,66,42],[95,66,42],[93,63,38],[112,82,56],[95,66,42],[88,55,26],[108,78,53],[84,52,22],[90,62,38],[93,63,38],[106,75,49],],[[90,62,38],[84,52,22],[86,55,27],[93,63,38],[88,55,26],[95,66,42],[70,40,10],[86,55,27],[95,66,42],[90,62,38],[102,73,48],[89,58,32],[88,55,26],[112,82,56],[95,66,42],[95,66,42],],[[102,73,48],[90,62,38],[88,55,26],[86,55,27],[95,66,42],[102,73,48],[112,82,56],[93,63,38],[131,106,88],[90,62,38],[86,55,27],[86,55,27],[100,69,42],[124,92,65],[108,78,53],[95,66,42],],[[93,63,38],[106,75,49],[84,52,22],[124,92,65],[88,55,26],[102,73,48],[108,78,53],[95,66,42],[95,66,42],[104,84,70],[86,55,27],[90,62,38],[102,73,48],[86,55,27],[93,63,38],[95,66,42],],[[100,69,42],[90,62,38],[90,62,38],[95,66,42],[95,66,42],[100,69,42],[95,66,42],[90,62,38],[95,66,42],[95,66,42],[95,66,42],[108,78,53],[89,58,32],[90,62,38],[84,52,22],[95,66,42],],[[93,63,38],[90,62,38],[86,55,27],[86,55,27],[131,106,88],[106,75,49],[100,69,42],[93,63,38],[95,66,42],[95,66,42],[90,62,38],[95,66,42],[100,69,42],[93,63,38],[95,66,42],[124,92,65],],[[93,63,38],[70,40,10],[95,66,42],[90,62,38],[104,84,70],[95,66,42],[93,63,38],[95,66,42],[88,55,26],[70,40,10],[93,63,38],[93,63,38],[95,66,42],[108,78,53],[93,63,38],[108,78,53],],[[95,66,42],[95,66,42],[95,66,42],[93,63,38],[88,55,26],[95,66,42],[112,82,56],[102,73,48],[88,55,26],[84,52,22],[102,73,48],[95,66,42],[112,82,56],[95,66,42],[106,75,49],[84,52,22],],[[102,73,48],[84,52,22],[102,73,48],[88,55,26],[100,69,42],[124,92,65],[112,82,56],[84,52,22],[112,82,56],[102,73,48],[89,58,32],[95,66,42],[108,78,53],[108,78,53],[102,73,48],[84,52,22],],[[124,92,65],[100,69,42],[108,78,53],[100,69,42],[88,55,26],[88,55,26],[95,66,42],[100,69,42],[108,78,53],[90,62,38],[84,52,22],[100,69,42],[131,106,88],[104,84,70],[93,63,38],[93,63,38],]],
	"grass_side": [[[70,121,29],[74,123,31],[58,101,23],[60,101,23],[68,118,28],[64,107,25],[60,104,24],[56,98,22],[57,100,22],[64,113,25],[66,113,25],[65,117,27],[63,106,24],[64,108,24],[59,102,24],[60,104,24],],[[67,116,28],[73,124,32],[69,119,29],[73,124,32],[74,123,31],[62,107,25],[61,105,25],[65,111,25],[66,118,28],[67,117,27],[66,113,25],[66,113,25],[65,111,25],[57,100,22],[56,98,22],[60,104,24],],[[65,109,25],[61,105,25],[68,118,28],[72,124,30],[68,119,27],[65,111,25],[66,113,25],[73,121,31],[67,117,27],[60,101,23],[65,111,25],[66,113,25],[68,118,28],[65,117,27],[58,101,23],[65,111,25],],[[68,118,28],[66,115,27],[61,106,24],[60,101,23],[65,111,25],[66,112,26],[65,111,25],[59,99,23],[56,98,22],[64,110,26],[68,117,29],[65,111,25],[66,118,28],[67,120,28],[66,118,28],[66,113,25],],[[62,107,25],[62,104,24],[56,98,22],[60,104,24],[74,124,30],[73,124,32],[68,118,28],[58,101,23],[62,104,24],[60,104,24],[60,104,24],[65,111,25],[64,107,25],[67,120,28],[69,120,28],[66,113,25],],[[70,120,30],[59,102,24],[60,104,24],[71,121,31],[73,124,32],[69,120,28],[62,107,25],[68,118,28],[73,121,31],[63,106,24],[57,99,23],[65,111,25],[66,113,25],[73,124,32],[64,110,26],[66,112,26],],[[57,99,23],[72,122,32],[60,104,24],[62,104,24],[68,119,27],[65,112,24],[64,110,24],[72,123,31],[74,123,31],[68,119,27],[67,116,28],[64,110,24],[63,112,24],[68,120,26],[74,123,31],[57,99,23],],[[68,118,28],[64,110,24],[64,110,24],[67,117,27],[66,118,28],[62,105,23],[64,110,24],[65,111,25],[61,105,25],[59,103,23],[65,117,27],[60,101,23],[62,112,26],[64,110,24],[65,109,25],[59,99,23],],[[74,124,30],[65,111,25],[65,111,25],[65,109,25],[67,116,28],[67,117,27],[70,121,29],[65,111,25],[60,104,24],[60,104,24],[65,117,27],[59,100,22],[56,98,22],[60,104,24],[61,105,25],[74,123,31],],[[65,117,27],[60,104,24],[74,123,31],[73,121,31],[58,101,23],[57,99,23],[61,106,24],[65,111,25],[66,115,27],[64,107,25],[64,110,24],[64,108,24],[59,102,24],[59,102,24],[62,107,25],[69,120,28],],[[60,101,23],[65,116,28],[69,120,28],[68,46,28],[57,99,23],[60,104,24],[60,104,24],[64,108,24],[65,111,25],[66,112,26],[65,111,25],[78,55,36],[62,107,25],[64,107,25],[73,122,30],[69,120,28],],[[67,117,27],[64,43,25],[58,101,23],[61,38,17],[60,104,24],[62,104,24],[56,98,22],[58,101,23],[68,46,28],[73,124,32],[64,110,26],[68,46,28],[63,106,24],[66,112,26],[68,46,28],[73,124,32],],[[64,110,24],[61,34,8],[83,57,36],[78,54,32],[65,111,25],[64,115,27],[66,44,25],[66,116,26],[77,47,22],[61,34,8],[81,54,32],[81,54,32],[67,116,28],[94,68,46],[81,54,32],[65,111,25],],[[83,57,36],[95,66,42],[95,66,42],[93,63,38],[77,47,22],[83,57,36],[98,71,48],[89,63,41],[88,55,26],[84,52,22],[102,73,48],[95,66,42],[98,71,48],[95,66,42],[106,75,49],[73,45,18],],[[102,73,48],[84,52,22],[102,73,48],[88,55,26],[100,69,42],[124,92,65],[112,82,56],[84,52,22],[112,82,56],[102,73,48],[89,58,32],[95,66,42],[108,78,53],[108,78,53],[102,73,48],[84,52,22],],[[124,92,65],[100,69,42],[108,78,53],[100,69,42],[88,55,26],[88,55,26],[95,66,42],[100,69,42],[108,78,53],[90,62,38],[84,52,22],[100,69,42],[131,106,88],[104,84,70],[93,63,38],[93,63,38],]],
	"grass_top": [[[70,121,29],[74,123,31],[58,101,23],[60,101,23],[68,118,28],[64,107,25],[60,104,24],[56,98,22],[57,100,22],[64,113,25],[66,113,25],[65,117,27],[63,106,24],[64,108,24],[59,102,24],[60,104,24],],[[67,116,28],[73,124,32],[69,119,29],[73,124,32],[74,123,31],[62,107,25],[61,105,25],[65,111,25],[66,118,28],[67,117,27],[66,113,25],[66,113,25],[65,111,25],[57,100,22],[56,98,22],[60,104,24],],[[65,109,25],[61,105,25],[68,118,28],[72,124,30],[68,119,27],[65,111,25],[66,113,25],[73,121,31],[67,117,27],[60,101,23],[65,111,25],[66,113,25],[68,118,28],[65,117,27],[58,101,23],[65,111,25],],[[68,118,28],[66,115,27],[61,106,24],[60,101,23],[65,111,25],[66,112,26],[65,111,25],[59,99,23],[56,98,22],[64,110,26],[68,117,29],[65,111,25],[66,118,28],[67,120,28],[66,118,28],[66,113,25],],[[62,107,25],[62,104,24],[56,98,22],[60,104,24],[74,124,30],[73,124,32],[68,118,28],[58,101,23],[62,104,24],[60,104,24],[60,104,24],[65,111,25],[64,107,25],[67,120,28],[69,120,28],[66,113,25],],[[70,120,30],[59,102,24],[60,104,24],[71,121,31],[73,124,32],[69,120,28],[62,107,25],[68,118,28],[73,121,31],[63,106,24],[57,99,23],[65,111,25],[66,113,25],[73,124,32],[64,110,26],[66,112,26],],[[57,99,23],[72,122,32],[60,104,24],[62,104,24],[68,119,27],[65,112,24],[64,110,24],[72,123,31],[74,123,31],[68,119,27],[67,116,28],[64,110,24],[63,112,24],[68,120,26],[74,123,31],[57,99,23],],[[68,118,28],[64,110,24],[64,110,24],[67,117,27],[66,118,28],[62,105,23],[64,110,24],[65,111,25],[61,105,25],[59,103,23],[65,117,27],[60,101,23],[62,112,26],[64,110,24],[65,109,25],[59,99,23],],[[74,124,30],[65,111,25],[65,111,25],[65,109,25],[67,116,28],[67,117,27],[70,121,29],[65,111,25],[60,104,24],[60,104,24],[65,117,27],[59,100,22],[56,98,22],[60,104,24],[61,105,25],[74,123,31],],[[65,117,27],[60,104,24],[74,123,31],[73,121,31],[58,101,23],[57,99,23],[61,106,24],[65,111,25],[66,115,27],[64,107,25],[64,110,24],[64,108,24],[59,102,24],[59,102,24],[62,107,25],[69,120,28],],[[60,101,23],[65,116,28],[69,120,28],[74,123,31],[57,99,23],[60,104,24],[60,104,24],[64,108,24],[65,111,25],[66,112,26],[65,111,25],[65,111,25],[62,107,25],[64,107,25],[73,122,30],[69,120,28],],[[67,117,27],[65,117,27],[58,101,23],[65,111,25],[60,104,24],[62,104,24],[56,98,22],[58,101,23],[74,123,31],[73,124,32],[64,110,26],[68,118,28],[63,106,24],[66,112,26],[72,123,31],[73,124,32],],[[64,110,24],[58,101,23],[59,100,22],[64,108,24],[65,111,25],[64,115,27],[58,101,23],[66,116,26],[69,120,28],[67,116,28],[63,106,24],[67,120,28],[67,116,28],[64,110,24],[65,111,25],[65,111,25],],[[65,111,25],[68,118,28],[66,118,28],[63,106,24],[65,111,25],[64,110,24],[64,110,24],[65,117,27],[67,117,27],[65,109,25],[66,118,28],[64,115,27],[70,120,30],[59,102,24],[60,104,24],[65,109,25],],[[60,101,23],[72,123,31],[69,120,28],[66,116,26],[60,104,24],[61,105,25],[65,111,25],[65,111,25],[60,104,24],[59,102,24],[62,104,24],[69,119,29],[74,123,31],[61,102,24],[58,100,24],[74,124,30],],[[65,111,25],[62,107,25],[67,117,27],[59,103,23],[60,104,24],[64,107,25],[74,123,31],[72,124,30],[57,99,23],[65,113,27],[72,123,31],[64,108,24],[64,108,24],[64,110,24],[66,118,28],[74,125,33],]],
	"stone": [[[143,143,143],[143,143,143],[143,143,143],[143,143,143],[127,127,127],[116,116,116],[116,116,116],[127,127,127],[116,116,116],[104,104,104],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[127,127,127],[127,127,127],],[[127,127,127],[127,127,127],[116,116,116],[127,127,127],[116,116,116],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[104,104,104],[104,104,104],[116,116,116],[127,127,127],[116,116,116],],[[127,127,127],[116,116,116],[104,104,104],[104,104,104],[116,116,116],[116,116,116],[116,116,116],[104,104,104],[116,116,116],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],],[[127,127,127],[127,127,127],[143,143,143],[143,143,143],[127,127,127],[143,143,143],[127,127,127],[127,127,127],[143,143,143],[143,143,143],[127,127,127],[127,127,127],[127,127,127],[116,116,116],[116,116,116],[116,116,116],],[[116,116,116],[127,127,127],[127,127,127],[116,116,116],[116,116,116],[116,116,116],[127,127,127],[116,116,116],[127,127,127],[143,143,143],[143,143,143],[143,143,143],[143,143,143],[116,116,116],[127,127,127],[127,127,127],],[[127,127,127],[143,143,143],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[116,116,116],[116,116,116],[104,104,104],[116,116,116],[104,104,104],[116,116,116],[143,143,143],],[[116,116,116],[127,127,127],[127,127,127],[143,143,143],[143,143,143],[143,143,143],[116,116,116],[143,143,143],[143,143,143],[116,116,116],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[127,127,127],[127,127,127],],[[116,116,116],[116,116,116],[104,104,104],[104,104,104],[116,116,116],[104,104,104],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[116,116,116],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[127,127,127],],[[143,143,143],[143,143,143],[143,143,143],[127,127,127],[143,143,143],[127,127,127],[127,127,127],[143,143,143],[143,143,143],[143,143,143],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[116,116,116],],[[127,127,127],[127,127,127],[143,143,143],[127,127,127],[127,127,127],[127,127,127],[143,143,143],[143,143,143],[143,143,143],[127,127,127],[127,127,127],[143,143,143],[143,143,143],[143,143,143],[143,143,143],[127,127,127],],[[104,104,104],[127,127,127],[116,116,116],[127,127,127],[116,116,116],[116,116,116],[104,104,104],[104,104,104],[116,116,116],[127,127,127],[116,116,116],[127,127,127],[127,127,127],[116,116,116],[116,116,116],[116,116,116],],[[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[143,143,143],[143,143,143],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[143,143,143],[143,143,143],[127,127,127],[143,143,143],],[[127,127,127],[116,116,116],[116,116,116],[116,116,116],[127,127,127],[143,143,143],[127,127,127],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[104,104,104],[104,104,104],[116,116,116],[104,104,104],[116,116,116],],[[143,143,143],[143,143,143],[127,127,127],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[116,116,116],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[116,116,116],[116,116,116],[116,116,116],[143,143,143],],[[127,127,127],[116,116,116],[116,116,116],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[143,143,143],[143,143,143],[143,143,143],[143,143,143],],[[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[116,116,116],[116,116,116],[127,127,127],[143,143,143],[143,143,143],[127,127,127],[127,127,127],[116,116,116],[127,127,127],[127,127,127],]],
	"wood": [[[133,105,60],[133,105,60],[133,105,60],[129,99,51],[161,126,72],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[161,126,72],[135,107,61],[133,105,60],[133,105,60],[133,105,60],[133,105,60],],[[82,63,35],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[82,63,35],[82,63,35],[82,63,35],[87,67,37],[87,67,37],[82,63,35],[82,63,35],[82,63,35],],[[126,96,48],[126,96,48],[87,67,37],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[126,96,48],[126,96,48],[133,105,60],[126,96,48],[126,96,48],],[[133,105,60],[126,96,48],[133,105,60],[133,105,60],[129,99,51],[157,121,69],[129,99,51],[126,96,48],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],],[[126,96,48],[161,126,72],[126,96,48],[126,96,48],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[137,107,61],[161,126,72],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],],[[82,63,35],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[82,63,35],[82,63,35],[82,63,35],[87,67,37],[87,67,37],[82,63,35],[82,63,35],[82,63,35],],[[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[161,126,72],[126,96,48],[126,96,48],[126,96,48],],[[126,96,48],[133,105,60],[133,105,60],[133,105,60],[126,96,48],[126,96,48],[126,96,48],[126,96,48],[126,96,48],[126,96,48],[126,96,48],[126,96,48],[126,96,48],[133,105,60],[133,105,60],[133,105,60],],[[126,96,48],[161,126,72],[166,129,74],[166,129,74],[157,121,69],[99,75,42],[129,99,51],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[126,96,48],],[[82,63,35],[82,63,35],[82,63,35],[82,63,35],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],],[[126,96,48],[126,96,48],[133,105,60],[133,105,60],[133,105,60],[137,107,61],[161,126,72],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[166,129,74],],[[126,96,48],[161,126,72],[166,129,74],[166,129,74],[166,129,74],[166,129,74],[161,126,72],[137,107,61],[133,105,60],[137,107,61],[161,126,72],[166,129,74],[166,129,74],[161,126,72],[133,105,60],[126,96,48],],[[166,129,74],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[137,107,61],[161,126,72],[161,126,72],[133,105,60],[99,75,42],[157,121,69],[161,126,72],[126,96,48],[166,129,74],],[[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[87,67,37],[82,63,35],[82,63,35],[87,67,37],[87,67,37],[87,67,37],],[[126,96,48],[126,96,48],[126,96,48],[129,99,51],[161,126,72],[166,129,74],[166,129,74],[157,121,69],[99,75,42],[157,121,69],[161,126,72],[129,99,51],[126,96,48],[126,96,48],[126,96,48],[126,96,48],],[[166,129,74],[166,129,74],[166,129,74],[161,126,72],[135,107,61],[133,105,60],[133,105,60],[133,105,60],[133,105,60],[126,96,48],[129,99,51],[161,126,72],[166,129,74],[166,129,74],[166,129,74],[166,129,74],]],
}

# Node definitions
nodes = {
	"dirt": ["dirt", "dirt", "dirt"],
	"grass": ["grass_side", "grass_side", "grass_top"],
	"stone": ["stone", "stone", "stone"],
	"wood": ["wood", "wood", "wood"]
}

### Drawing functions
def pixel(color, dir):
	ANGLES = {
		"right": [120, 60],
		"left": [60, 120]
	}
	cursor.color(color)
	cursor.pendown()
	cursor.begin_fill()
	for _ in range(2):
		cursor.forward(PIXEL)
		cursor.right(ANGLES[dir][0])
		cursor.forward(PIXEL)
		cursor.right(ANGLES[dir][1])
	cursor.end_fill()
	cursor.penup()

def plane(tile, dir, light):
	ANGLES = {
		"right": 120,
		"left": 60
	}
	A = ANGLES[dir]
	for y in range(16):
		for x in range(16):
			rgb = tile[y][x]
			pixel(value(rgb, light), dir)
			cursor.forward(PIXEL)
		cursor.backward(METER)
		cursor.right(A)
		cursor.forward(PIXEL)
		cursor.left(A)
	cursor.right(A)
	cursor.backward(METER)
	cursor.left(A)

def cube(tiles, position, cull):
	pos = isoToScreen(position[0], position[1], position[2])
	cursor.setposition(pos[0], pos[1] - METER / 2)

	cursor.seth(30)
	if not cull[0]:
		plane(textures[tiles[0]], "right", 0) # Right side

	cursor.seth(150)
	cursor.forward(METER)
	cursor.seth(-30)
	if not cull[1]:
		plane(textures[tiles[1]], "left", -0.15) # Left side

	cursor.seth(30)
	if not cull[2]:
		plane(textures[tiles[2]], "left", 0.15) # Top

	cursor.seth(0)
	screen.update()

### World data (y up, z right, x left)
world = [
	[
		[1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1],
	],
	[
		[1, 1, 1, 1, 1, 1, 1, 2],
		[1, 1, 1, 1, 1, 1, 1, 2],
		[1, 1, 1, 1, 1, 1, 1, 2],
		[1, 1, 1, 1, 1, 1, 2, 2],
		[1, 1, 1, 1, 1, 1, 2, 2],
		[1, 1, 1, 1, 1, 2, 2, 2],
		[1, 1, 1, 1, 2, 2, 2, 2],
		[1, 1, 2, 2, 2, 2, 2, 2],
	],
	[
		[1, 1, 1, 1, 1, 1, 1, 3],
		[1, 1, 1, 1, 1, 1, 1, 3],
		[1, 1, 1, 1, 1, 1, 1, 3],
		[1, 1, 1, 1, 1, 1, 3, 3],
		[1, 1, 1, 1, 1, 1, 3, 3],
		[1, 1, 1, 1, 1, 3, 3, 3],
		[1, 1, 1, 1, 3, 3, 3, 3],
		[2, 2, 3, 3, 3, 3, 3, 3],
	],
	[
		[1, 1, 1, 1, 1, 3, 3, 0],
		[1, 1, 1, 1, 3, 3, 3, 0],
		[1, 1, 3, 3, 3, 3, 3, 0],
		[3, 3, 3, 3, 3, 3, 0, 0],
		[3, 3, 3, 3, 3, 3, 0, 0],
		[3, 3, 3, 3, 3, 0, 0, 0],
		[3, 3, 3, 3, 0, 0, 0, 0],
		[3, 3, 0, 0, 0, 0, 0, 0],
	],
	[
		[3, 3, 3, 3, 3, 0, 0, 0],
		[3, 3, 3, 3, 0, 0, 0, 0],
		[3, 3, 4, 0, 0, 0, 0, 0],
		[4, 0, 4, 0, 0, 0, 0, 0],
		[4, 0, 0, 0, 0, 0, 0, 0],
		[4, 4, 4, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
	],
	[
		[0, 0, 0, 0, 0, 0, 0, 0],
		[4, 4, 4, 0, 0, 0, 0, 0],
		[4, 0, 4, 0, 0, 0, 0, 0],
		[4, 0, 4, 0, 0, 0, 0, 0],
		[4, 0, 0, 0, 0, 0, 0, 0],
		[4, 0, 4, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
	],
	[
		[0, 0, 0, 0, 0, 0, 0, 0],
		[4, 4, 4, 0, 0, 0, 0, 0],
		[4, 4, 4, 0, 0, 0, 0, 0],
		[4, 4, 4, 0, 0, 0, 0, 0],
		[4, 4, 4, 0, 0, 0, 0, 0],
		[4, 4, 4, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
	],
]

node_map = [
	"air",
	"stone",
	"dirt",
	"grass",
	"wood",
]

### World functions
def isAir(pos):
	try:
		v = world[pos[1]][pos[2]][pos[0]] # (1, 2, 0) because the world is stored in (y, z, x) format
	except IndexError:
		v = 0
	return v == 0

# Cull nodes that cant be seen due to other nodes blocking them (not perfect)
def isoCull(pos):
	x = pos[0]
	y = pos[1]
	z = pos[2]
	for _ in range(len(world) - min(x, z)):
		x += 1
		y += 1
		z += 1
		if not isAir([x, y, z]):
			return True
	return False

def node(name, pos):
	if name == "air" or isoCull(pos):
		return

	x = pos[0]
	y = pos[1]
	z = pos[2]

	cull = [
		not isAir([x + 1, y, z]),
		not isAir([x, y, z + 1]),
		not isAir([x, y + 1, z])
	]

	cube(nodes[name], [x, y + 2, z], cull)

### Set up window
PAD = METER * 4
WIDTH = max(len(world[0]), len(world[0][0])) * METER * 2 + PAD
HEIGHT = len(world) * METER * 2 + PAD
screen.setup(width = WIDTH, height = HEIGHT)

### Map generation
for y in range(len(world)):
	for z in range(len(world[y])):
		for x in range(len(world[y][z])):
			node(node_map[world[y][z][x]], [x, y, z])

### End
screen.exitonclick()
