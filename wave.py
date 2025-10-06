"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Kiyam Merali km942, Eben Hill emh238
12/03/2023
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _dead: a bool relating whether or not the ship just died
    # Invariant: _dead is a boolean
    #
    # Attribute _nextshot: the number of moves until the next alien shoots
    # Invariant: _nextshot is an int >= 0
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getDead(self):
        """
        Returns the _dead attribute for the current wave object
        """
        return self._dead

    def getAliens(self):
        """
        Returns the _aliens attribute for the current wave class (2D list
        containing Alien objects or None)
        """
        return self._aliens

    def getLives(self):
        """
        Returns the number of lives the player has left (int)
        """
        return self._lives

    def setDead(self,b):
        """
        Sets _dead to parameter b

        Parameter b: the truth value of the dead attribute
        Precondition: b is a boolean
        """
        assert isinstance(b,bool)
        self._dead=b

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes an object of the wave class
        """
        self._ship=Ship()
        x_cor_al=(ALIEN_H_SEP+(ALIEN_WIDTH/2))
        y_cor_al=GAME_HEIGHT-(ALIEN_CEILING+(ALIEN_HEIGHT/2))
        self._aliens=self._alien_2d(x_cor_al,y_cor_al,ALIENS_IN_ROW,ALIEN_ROWS,
        ALIEN_IMAGES[0])
        self._bolts=[]
        #defense line
        self._dline=GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
        linewidth=1,linecolor='red')
        self._lives=SHIP_LIVES
        self._time=0
        self._direction=True #right, False means left
        self._dead=False
        self._nextshot=random.randint(1,BOLT_RATE)

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Updates a frame in the game. Updates the position of the ship, aliens,
        and laser bolts, and checks for collisions.

        Parameter input: user input controlling ship and bolts
        Precondition: input is an instance of GInput.

        Parameter dt: time in seconds since the last call to update
        Precondition: dt is a float >= 0
        """
        assert isinstance(input, GInput)
        assert isinstance(dt, float)
        assert dt >= 0

        if self._ship.getShipX() <= GAME_WIDTH:
            if input.is_key_down('right'):
                self._ship.moveShip(SHIP_MOVEMENT)
        if self._ship.getShipX() >= 0:
            if input.is_key_down('left'):
                self._ship.moveShip(-SHIP_MOVEMENT)
        if self._time > ALIEN_SPEED:
            self.horde_move(ALIEN_H_WALK,ALIEN_V_WALK)
            self._nextshot-=1
            self._time=0
        else:
            self._time+=dt
        if input.is_key_pressed('spacebar'):
            if self.no_player_bolt()==True:
                self.ship_fire_bolt()
        for bolt in self._bolts:
            bolt.moveBolt()
        for bolt in self._bolts:
            if bolt.bottom > GAME_HEIGHT or bolt.top<0:
                del self._bolts[self._bolts.index(bolt)]

        self.resolve_alien_shots()
        self.resolve_alien_collisions()
        self.resolve_ship_collisions()
        self.update_lives()

    def no_player_bolt(self):
        """
        Returns True if there are no player bolts on the screen
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                return False
        return True

    def resolve_alien_shots(self):
        """
        Has the aliens shoot after the countdown from their last shot
        """
        if self._nextshot == 0:
            self.alien_fire_bolt()
            self._nextshot=random.randint(1,BOLT_RATE)

    def resolve_alien_collisions(self):
        """
        Resolves bolt collisions with aliens
        """
        for bolt in self._bolts:
            for row in self._aliens:
                for alien in row:
                    if alien is not None and bolt.collides(alien)\
                     and bolt.isPlayerBolt():
                        row[row.index(alien)]= None
                        del self._bolts[self._bolts.index(bolt)]

    def resolve_ship_collisions(self):
        """
        Resolves bolt collisions with the ship
        """
        for bolt in self._bolts:
            if self._ship != None:
                if bolt.collides(self._ship):
                    self._ship = None
                    del self._bolts[self._bolts.index(bolt)]

    def update_lives(self):
        """
        If ship is killed reduces lives by one and set self._dead to true
        """
        if self._ship is None:
            self._lives = self._lives - 1
            self._dead=True

    def respawn_ship(self):
        """
        Respawns the ship at the center of board
        """
        if self._lives > 0:
            self._ship = Ship()

    def assert_win_conditions(self):
        """
        Returns True if win conditions are present
        """
        if self.all_aliens_dead():
            return True
        else:
            return False

    def assert_lose_conditions(self):
        """
        Returns True if lose conditions are present
        """
        if self.alien_below_line() == True:
            return True
        elif self._lives==0:
            return True
        else:
            return False

    #helper for moving aliens
    def horde_move(self,incr_x,incr_y):
        """
        Moves all the aliens, changing direction when they reach the edge

        Parameter incr_x: the magnitude of each alien's movement on the x-axis
        Precondition: incr_x is a positive number

        Parameter incr_y: the magnitude of each alien's movement on the y-axis
        Precondition: incr_y is a positive number
        """
        assert isinstance(incr_x,int) or isinstance(incr_x,float)
        assert isinstance(incr_y,int) or isinstance(incr_y,float)
        assert incr_y >= 0 and incr_x >= 0
        #check closest to end alien
        for row in self._aliens:
            #moving aliens right
            if self._direction==True:
                if not self.check_last_alien(row) == False:
                    self.move_row_right(row,incr_x,incr_y)
            #moving aliens left
            elif self._direction==False:
                if not self.check_last_alien(row) == False:
                    self.move_row_left(row,incr_x,incr_y)

    def move_row_right(self,row,incr_x,incr_y):
        """
        Moves a row of aliens to the right (or down if too far right)

        Parameter incr_x: the magnitude of each alien's movement on the x-axis
        Precondition: incr_x is a positive number

        Parameter incr_y: the magnitude of each alien's movement on the y-axis
        Precondition: incr_y is a positive number
        """
        assert isinstance(incr_x,int) or isinstance(incr_x,float)
        assert isinstance(incr_y,int) or isinstance(incr_y,float)
        assert incr_y >= 0 and incr_x >= 0
        #the aliens have gone too far right...
        if (GAME_WIDTH-row[self.check_last_alien(row)].x) < ALIEN_H_SEP:
            self._direction = False
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.moveAlienY(-incr_y)
        #keep moving father right wretched aliens!
        else:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        if self._direction == True: #True if going right
                            alien.moveAlienX(incr_x)

    def move_row_left(self,row,incr_x,incr_y):
        """
        Moves a row of aliens to the left (or down if too far left)

        Parameter incr_x: the magnitude of each alien's movement on the x-axis
        Precondition: incr_x is a positive number

        Parameter incr_y: the magnitude of each alien's movement on the y-axis
        Precondition: incr_y is a positive number
        """
        assert isinstance(incr_x,int) or isinstance(incr_x,float)
        assert isinstance(incr_y,int) or isinstance(incr_y,float)
        assert incr_y >= 0 and incr_x >= 0
        #commie aliens must stop somewhere
        if row[self.check_first_alien(row)].x < ALIEN_H_SEP:
            self._direction = True
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.moveAlienY(-incr_y)
        #aliens moving farther and farther to the left
        else:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        if self._direction == False: #True if going left
                            alien.moveAlienX(-incr_x)

    def check_last_alien(self,row):
        """
        Returns (negative) position of final alien in row if it exists
        Otherwise returns False

        Parameter row: row is a row of Aliens
        Precondition: row is a list
        """
        assert isinstance(row,list)
        if self.is_empty_row(row) == True:
            return False
        last_alien=-1
        while row[last_alien] == None:
            last_alien-=1
        return last_alien

    def is_empty_row(self,row):
        """
        Returns True if row is "empty" (all Nones), otherwise returns False

        Parameter row: row is a row of Aliens
        Precondition: row is a list
        """
        assert isinstance(row,list)
        row_empty=True
        for alien in row:
            if not alien == None:
                row_empty=False
        return row_empty

    def check_first_alien(self,row):
        """
        Returns (positive) position of first alien in row if it exists
        Otherwise returns False

        Parameter row: row is a row of Aliens
        Precondition: row is a list
        """
        assert isinstance(row,list)
        if self.is_empty_row(row) == True:
            return False
        first_alien=0
        while row[first_alien] == None:
            first_alien+=1
        return first_alien

    def ship_fire_bolt(self):
        """
        Fires a laser bolt from the ship

        Creates a Bolt object at the ship's position and adds it to the list of
        bolts.
        """
        x_cor=self._ship.x
        y_cor=self._ship.top
        blt=Bolt()
        blt.x=x_cor
        blt.y=y_cor
        self._bolts.append(blt)

    def alien_fire_bolt(self):
        """
        Fires a laser bolt from a random alien ship.
        """
        col =self.non_empty_column()
        if col is not None:
            row = len(self._aliens) - 1
            bottom_alien=None

            while row>= 0 and bottom_alien==None:#no infinite loop plz
                alien = self._aliens[row][col]
                if alien is not None:
                    bottom_alien = alien
                row = row-1

            if bottom_alien is not None:
                x_cor = bottom_alien.x
                y_cor = bottom_alien.y - BOLT_HEIGHT / 2
                blt=Bolt()
                blt.x=x_cor
                blt.y=y_cor
                self._bolts.append(blt)
                blt._velocity = -BOLT_SPEED

    def non_empty_column(self):
        """
        Helper for alien_fire_bolt. Selects a non-empty column from alien grid
        at random.
        Returns the index of column or None if all columns are empty.
        """
        acum=[]
        for col in range(ALIENS_IN_ROW):
            has_alien=False
            for row in self._aliens:
                if row[col] is not None: #check for alien
                    has_alien = True
            if has_alien==True:
                acum.append(col)

        if len(acum)>0:
            return random.choice(acum)
        return None

#helpers for game completion
    def all_aliens_dead(self):
        """
        Checks if all aliens in the wave have been killed. Returns True if they
        have all been killed, or False if they haven't all been killed yet.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    return False

        return True

    def alien_below_line(self):
        """
        Checks if alien crosses below the defense line. Returns true if an alien
        has a position below the defense line
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    if alien.y < DEFENSE_LINE:
                        return True
        return False

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws ships, aliens, defensive line and bolts

        Parameter view: View to draw the objects in
        Precondition: view is a GView object
        """
        assert isinstance(view,GView)
        #drawing aliens
        for row in self.getAliens():
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        #drawing ship
        if self._ship is not None:
            self._ship.draw(view)
        #drawing defensive line
        self._dline.draw(view)
        #drawing bolts
        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def _alien_2d(self,x,y,num_col,num_rows,src):
        """
        Returns a 2d list of aliens with the type alternating every two rows

        Parameter x: x coordinate of first alien in grid
        Precondition: x is a float or int

        Parameter y: y coordinate of first alien in grid
        Precondition: y is a float or int

        Parameter num_col: number of columns in the grid
        Precondition: int, >0

        Parameter num_rows: number of rows in the grid
        Precondition: int, >0

        Parameter src: alien image file
        Precondition: str that refers to an image file
        """
        assert isinstance(x,float) or isinstance (x, int)
        assert isinstance(y,float) or isinstance (y, int)
        assert isinstance(num_col, int) and num_col >0
        assert isinstance(num_rows, int) and num_rows >0
        assert isinstance(src, str)

        ycor_accum=y
        j=0
        png_accum1=0
        png_bool=False
        list_accum=[]
        while j < num_rows:
            list_accum.append(alien_row(x,ycor_accum,ALIEN_IMAGES[png_accum1],num_col))
            ycor_accum=ycor_accum-(ALIEN_HEIGHT+ALIEN_V_SEP)
            if png_bool:
                png_accum1+=1
                png_bool=False
            else:
                png_bool=True
            j+=1
            if png_accum1==3:
                png_accum1=0
        return list_accum
