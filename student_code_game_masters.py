from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # ask what disks are on what peg in the KB
        P1 = self.kb.kb_ask(parse_input('fact: (on ?disk peg1'))
        P2 = self.kb.kb_ask(parse_input('fact: (on ?disk peg2'))
        P3 = self.kb.kb_ask(parse_input('fact: (on ?disk peg3'))
        p1 = []
        p2 = []
        p3 = []

        # Disks on peg1
        if P1:
            for disks in P1:
                # get the name and take the last index for the number
                disk = int(str(disks.bindings[0].constant)[-1])
                # append it to the array
                p1.append(disk)
            # sort array
            p1.sort()
        # repeat for the next two pegs

        # Disks on peg2
        if P2:
            for disks in P2:
                disk = int(str(disks.bindings[0].constant)[-1])
                p2.append(disk)
            p2.sort()

        # Disks on peg3
        if P3:
            for disks in P3:
                disk = int(str(disks.bindings[0].constant)[-1])
                p3.append(disk)
            p3.sort()

        # Append the tuples together

        game_state = (tuple(p1), tuple(p2), tuple(p3))
        return game_state
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # Get the terms out of the statement
        disk = str(movable_statement.terms[0])
        init_peg = str(movable_statement.terms[1])
        fin_peg = str(movable_statement.terms[2])

        # Retract the facts from the KB
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + init_peg + ")"))
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + init_peg + ")"))

        multiple = self.kb.kb_ask(parse_input("fact: (onTopOf " + disk + " ?d)"))
        if multiple:
            below_disk = str(multiple[0].bindings[0].constant)
            self.kb.kb_retract(parse_input("fact: (onTopOf " + disk + " " + below_disk + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + below_disk + " " + init_peg + ")"))
        else:
            self.kb.kb_assert(parse_input("fact: (empty " + init_peg + ")"))

        # We know for sure that the disk is on the fin_peg
        self.kb.kb_assert(parse_input("fact: (on " + disk + " " + fin_peg + ")"))

        # If fin peg was initially empty, it no longer is. Additionally, disk is for sure top of fin_peg
        fin_empty = self.kb.kb_ask(parse_input("fact: (empty " + fin_peg + ")"))
        if fin_empty:
            self.kb.kb_retract(parse_input("fact: (empty " + fin_peg + ")"))
        # if it's not empty, old "top" disk on fin_peg is no longer on top
        else:
            init_ontop = self.kb.kb_ask(parse_input("fact: (top ?disk " + fin_peg + ")"))
            if init_ontop:
                init_topdisk = init_ontop[0].bindings[0].constant
                self.kb.kb_retract(parse_input("fact: (top " + str(init_topdisk) + " " + fin_peg + ")"))
                self.kb.kb_assert(parse_input(("fact: (onTopOf " + disk + " " + str(init_topdisk) + ")")))

        # Now assert that disk is on the top of fin_peg
        self.kb.kb_assert(parse_input("fact: (top " + disk + " " + fin_peg + ")"))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
