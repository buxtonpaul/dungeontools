# Dungeon Mapping tools

Generating Random dungeon maps for use in D&D style games.

There are several aspects to this.
1. Generating a random map
2. Letting a user modify it
3. Rendering it in a way that can be used in games

We can satisfy 2 by storing the map as a editable text file using different characters to show filled or empty space


## Generating a random map

Some useful info [here][1] and [here][2]

We have implemented a python version in [dungeonmap.py](./dungeonmap.py)

Using the scheme above produces reasonable looking map e.g.
```
################################################################################
####      #################   ##########  ######         ##########   ##########
###                            ########   ######          ########        ######
##                                  ##    #############    ######          #####
##                  #####                ###############                   #####
##         ###     #######             ##########   ####                   #####
###        ###     #######      #############        ####   ######          ####
###                ########    ############          ##############          ###
###                #########  ###########      ###   ##############           ##
##   ##           ######################      #####  ###############          ##
#   ##            #####################       #####  ################    ###  ##
#   ##            #############    ####        ###   ########################  #
#                 ############      ###     #         #######################  #
#                #############      ####   ###              #######   #######  #
##            ################      #####  ####              #####      ####   #
##        ####################      ######  ####             #####             #
##   #   #####################      #######  #####          ######             #
##  ###  #############  #######     #######   #####        #######     ####    #
##  ###  ############     #####      ######    #####   ############    ####    #
##   #   ############       ##        ######   ######################          #
##       #############                 ###############################         #
##        ############           ##    ###############################        ##
##        ############            #    ############    ###############        ##
##     #   ###########                 ###########      #############         ##
##    ###   #########      ##         ############              ####          ##
##     ###   ######       ####     ###############   ##          ###           #
##     ###   #####       #########################  ####          ###          #
##     ###   ####        #########################  ######        ###          #
##          ###           #################    ##    #####        ####        ##
##         ###      ###   ####### ########                        #####       ##
##        ####     #####  ######   ####                      ##    ########   ##
#        #####     #####  #####    ###          ####        ###     ########  ##
#       ######      ####           ###    ###  #######    #####     ########  ##
#       #######      ##           ####   ####  ########  #####      ########  ##
#        #######                 #####   ####  ###############       ######   ##
#           ###                  ####     ##    #######  ####           ##    ##
#                                 ##            ###            ##            ###
#      #####            ###                    ####           ####   ###   #####
##    #######  #############  ###   ############################################
################################################################################

```





## Rendering a map

Given a tile map like that above we need to turn this into graphics. The tile map above shows areas that are filled or not.
We could either
- Use premade graphics that we place according to the wall layout. E.g. premade tiles that we rotate and join up
- Use map and make it more intersting looking through applying filters and procedural generaation techniques the map interesting.

If we treat the base map as a mask we can then produce an image through applying mask and blend operations. Using various sources of image data.

E.g. given an image that looks like stone floor we can use a mask to apply this only to the area that should be stone.
We can either load textures from file, but they either need to be high enough resolution, or tesselate well.
An alternative is to generate the textures. This is commonly used in 3d graphics and film fx. The most common usages is based on Perlin noise, see links below.


In psuedo code it might look something like

We basically have either
- Masks , a monochrome layer with range from 0-1 (with our base map being the first example)
- colortype
  - Colors, a solid color
  - Textures, image data read from a file or the result of blend operator
- Blend operator, take two colortypes and blend according to the mask type
- Mask operator. Perform operations on the Mask inclusing:
  - LUT type operations
  - Image processing type (e.g. Edge Detect)
  - Distort

So the creation of a map can be see as something like 
```
convert the map into a mask
Apply distorion to mask (to make it a bit rough)
Create sand texture as blend between perlin noise and brown+beige
Crate stone texture as blend betwen perlin noise and grey,darkgrey
Create Slab texture as blend worley noise using stone and sand
create map texture as blend between dungeon mask with black and slab
```

Some refernence on blending operations [here][6]
The distortion can be done with something like  [this][4] it again uses Noise, but the noise is used to provide smoothly varying random x and y vectors which are used to map coordinates from an output image to the source image.
E.g. for each pixel (x,y) in the output image we fetch it from x+noise(x),y+noise(y)


Also useful for blending between textures [here][5]

Some code for generating Perlin Noise
```Python
from noise import pnoise2, snoise2
import matplotlib.pyplot as plt
%matplotlib inline
noisetile=[]
octaves=16
freq=25
for y in range(256):
    noisetile.append([])
    for x in range(256):
        noisetile[-1].append(snoise2(x / freq, y / freq, octaves))
plt.imshow(noisetile,cmap='gray')
```

Perhaps also look at [Noisemaker][7]


## Some other links on Perlin Noise

- https://eev.ee/blog/2016/05/29/perlin-noise/
- https://rmarcus.info/blog/2018/03/04/perlin-noise.html
- http://flafla2.github.io/2014/08/09/perlinnoise.html
- http://www.andysaia.com/radicalpropositions/perlin-noise-flow-fields/
- https://gamedev.stackexchange.com/questions/23625/how-do-you-generate-tileable-perlin-noise
- https://gist.github.com/eevee/26f547457522755cb1fb8739d0ea89a1
- https://medium.com/@yvanscher/playing-with-perlin-noise-generating-realistic-archipelagos-b59f004d8401
- https://gpfault.net/posts/perlin-noise.txt.html

The mechanism for distoring an image slightly is to generate two noise fields which are used as x and y vectors for deforming the image.


## Status
Now create a map and shows it in a window rendered with a simple 'sand' texture

- [x] Get the generator to output the data in a more useful format for downstream consumption
- [x] Which image related library to use? OpenCV Pillow, Scipy?

![Sample][SampleImage]


## Other stuff to do
- [ ] Implement texture API to allow easy creation/use of textures
- [ ] Prototype distorsion
- [ ] Add other noise and parametrise it on the API
- [ ] Other ways of generating dungeons (random walks)
- [ ] Visualising textures. The set of operations would basically be a graph with nodes for blend etc.
- [ ] Texture presets
- [ ] Tesselating image textures  (mirror?)
- [ ] Implement unit tests!
- [ ] Some form of CI (Azure pipelines or Travis? ) to run unit tets
 



[1]: http://roguebasin.roguelikedevelopment.org/index.php?title=Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
[2]: https://donjon.bin.sh/code/dungeon/
[3]: https://gpfault.net/posts/perlin-noise.txt.html
[4]: https://observablehq.com/@kerryrodden/image-distortion-with-perlin-noise 
[5]: http://devmag.org.za/2009/04/25/perlin-noise/
[6]: https://note.nkmk.me/en/python-opencv-numpy-alpha-blend-mask/
[7]: https://noisemaker.readthedocs.io/en/latest/
[sampleimage]: ./output.jpg