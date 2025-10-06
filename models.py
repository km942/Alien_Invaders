"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Kiyam Merali km942, Eben Hill emh238
12/05/2023
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShipX(self):
        """
        Returns x position of ship
        """
        return self.x

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Initializes a ship object appearing at the bottom middle of the screen
        """
        super().__init__(x=(GAME_WIDTH/2),width=SHIP_WIDTH,height=SHIP_HEIGHT,\
        source=SHIP_IMAGE,bottom=SHIP_BOTTOM)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveShip(self,incr):
        """
        Moves the ship an amount equal to the magnitude of parameter incr
        Negative values move the ship left and vice versa

        Parameter incr: increment to change x position by
        Precondition: incr is a float or an int
        """
        assert isinstance(incr,float) or isinstance(incr,int)
        self.x+=incr

    def collides(self,bolt):
        """
        Returns True if alien bolt collides with ship, returns False if
        bolt was not fired by an alien.

        Parameter bolt: bolt is a Bolt object
        Precondition: bolt is a Bolt object (redundant, I know)
        """
        assert isinstance(bolt,Bolt)

        if bolt.getVelocity()>0:
            return self.contains((bolt.x,bolt.y))
        else:
            return False


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,source=ALIEN_IMAGES[0]):
        """
        Initializes some alien dudes

        Parameter x: the x value of the center of the alien
        Precondition: x is a positive number or zero

        Parameter y: the y value of the center of the alien
        Precondition: y is a positive number or zero

        Parameter source: an image file to be displayed as the alien
        Precondition: source is a string
        """
        assert isinstance(x,int) or isinstance(x,float)
        assert isinstance(y,int) or isinstance(y,float)
        assert isinstance(source,str)

        super().__init__(x=x,y=y,width=ALIEN_WIDTH,\
        height=ALIEN_HEIGHT,source=source)

    def moveAlienX(self,incr):
        """
        Moves the alien on the x axis by incr

        Parameter incr: increment to change x position by
        Precondition: incr is a float or an int
        """
        assert isinstance(incr,float) or isinstance(incr,int)
        self.x+=incr

    def moveAlienY(self,incr):
        """
        Moves the alien on the y axis by incr

        Parameter incr: increment to change y position by
        Precondition: incr is a float or an int
        """
        assert isinstance(incr,float) or isinstance(incr,int)
        self.y+=incr

    def collides(self,bolt):
        """
        Returns True if bolt collides with alien, returns false if bolt was
        not fired by the player

        Parameter bolt: bolt is a Bolt object
        Precondition: bolt is a bolt object (redundancy part 2)
        """
        assert isinstance(bolt,Bolt)

        if bolt.getVelocity()<0:
            return self.contains((bolt.x,bolt.y))
        else:
            return False


def alien_row(x,y,src,num):
    """
    Returns a row of aliens of the specified type
    The aliens will be ALIEN_H_SEP apart from each other

    There will be ALIENS_IN_ROW aliens in every row

    Parameter x: The horizontal position of the first alien (far left) in row
    Precondition: x is a positive int or float

    Parameter y: The vertical position of the first alien in row
    Precondition: y is a positive number

    Parameter src: The aliens' source (file.png)
    Precondition: src is a string corresponding to a png file

    Parameter num: The number of aliens to be generated in row
    Precondition: num is an int and is not overstepping possible bounds
    """
    assert isinstance(x,int) or isinstance(x,float) and x > 0
    assert isinstance(y,int) or isinstance(y,float) and y > 0
    assert isinstance(src,str)
    assert isinstance(num,int)
    xcor_accum=x
    list_accum=[]
    j=0
    while j < num:
        list_accum.append(Alien(xcor_accum,y,source=src))
        xcor_accum+=(ALIEN_H_SEP+ALIEN_WIDTH)
        j+=1
    return list_accum


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns _velocity attribute of Bolt object
        """
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self):
        """
        Creates a Bolt() object
        """
        super().__init__(x=0,y=0,width=BOLT_WIDTH,height=BOLT_HEIGHT,\
        fillcolor='blue',linecolor='blue')
        self._velocity=BOLT_SPEED

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def moveBolt(self):
        """
        Moves the bolt in a direction and magnitude specified by _velocity
        """
        self.y+=self._velocity

    def isPlayerBolt(self):
        """
        Returns True if _velocity is positive
        """
        if self._velocity > 0:
            return True
        else:
            return False

    def collides(self, obj):
        """
        Returns True if colt collides with object obj

        Parameter obj: obj is any object
        Precondition: obj is an object
        """
        return obj.contains((self.x,self.y))
