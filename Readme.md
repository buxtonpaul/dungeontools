# Dungeon Mapping tools

Generating Random dungeon maps for use in D&D style games.

There are several aspects to this.
- Generating a random map
- Letting a user modify it
- Rendering it in a way that can be used in games


## Generating a map

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

### Todo 

- Look into other genreation techniques, to maybe do different styles
- Add function to get data as something more useful for graphics processing




## Rendering a map

Given a tile map like that above we need to turn this into graphics. The tile map above shows areas that are filled or not.
We could either
- Use premade graphics that we place according to the wall layout. E.g. premade tiles that we rotate and join up
- Use map and make it more intersting looking through applying filters to the edges etc to make them more organic. This may still need some analysis of surrounding tiles to fill in the tiles to follow the shape of the wall without being to blocky

Could we use some fractal landscape type solution where we treat some of the points from the base map as fixed segments and peturb the inbetween points?

1. create a simple canvas and fill it according to the map. This should be able to read in maps that are simply text files so that we can try with the same map, and allow users to edit the map easily
2. Render the map as a simple output png with tiles of a given x,y dimension
3. Apply some stuff to the image to provide an organic feel [(perlin noise perhaps?)][4]
4. Generate textures to use for floor [(again noise looks good for this)][3]
5. Possibly use different noise for stone edges...


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


Thinking on this some more I think most of it can be done as a series of blend operations.
We basically have either
- Masks , a monochrome layer with range from 0-1
- colortype
  - Colors, a solid color
  - Textures, image data read from a file or the result of blend operator
- Blend operator, take two colortypes and blend according to the mask type
- Mask operator. Perform operations on the Mask inclusing:
  - LUT type operations
  - Image processing type (e.g. Edge Detect)
  - Distort

So the creation of a map can be see as something like convert the map into a mask
Apply distorion to mask (to make it a bit rough)
Create sand texture as blend between perlin noise and brown+beige
Crate stone texture as blend betwen perlin noise and grey,darkgrey
Create Slab texture as blend worley noise using stone and sand
create map texture as blend between dungeon mask with black and slab

Some refernence on blending operations [here][6]

## Some other links on Perlin Noise

- https://eev.ee/blog/2016/05/29/perlin-noise/
- https://rmarcus.info/blog/2018/03/04/perlin-noise.html
- http://flafla2.github.io/2014/08/09/perlinnoise.html
- http://www.andysaia.com/radicalpropositions/perlin-noise-flow-fields/
- https://gamedev.stackexchange.com/questions/23625/how-do-you-generate-tileable-perlin-noise
- https://gist.github.com/eevee/26f547457522755cb1fb8739d0ea89a1
- https://medium.com/@yvanscher/playing-with-perlin-noise-generating-realistic-archipelagos-b59f004d8401

The mechanism for distoring an image slightly is to generate two noise fields which are used as x and y vectors for deforming the image.

## Other stuff to do

- [ ] Other ways of generating dungones
- [ ] Visualising textures
- [ ] Texture presets
- [ ] Tesselating image textures  (mirror?)


[1]: http://roguebasin.roguelikedevelopment.org/index.php?title=Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels
[2]: https://donjon.bin.sh/code/dungeon/
[3]: https://gpfault.net/posts/perlin-noise.txt.html
[4]: https://observablehq.com/@kerryrodden/image-distortion-with-perlin-noise 
[5]: http://devmag.org.za/2009/04/25/perlin-noise/
[6]: https://note.nkmk.me/en/python-opencv-numpy-alpha-blend-mask/
[7]: https://noisemaker.readthedocs.io/en/latest/