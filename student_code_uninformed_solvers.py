
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def findNextStep(self):
        # If we still have child nodes we have not visited
        if self.currentState.nextChildToVisit < len(self.currentState.children):
            # We need to check if we have already visited the child
            if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                current_state = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.currentState = current_state
                self.gm.makeMove(self.currentState.requiredMovable)
                return
            else:  # if we have already visited, visit the next child
                self.currentState.nextChildToVisit += 1
                self.findNextStep()
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.findNextStep()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Student code goes here
        cs = self.currentState
        self.visited[cs] = True

        # If already in correct state then return True
        if self.currentState.state == self.victoryCondition:
            return True

        moves = self.gm.getMovables()

        if moves:
            for move in moves:
                self.gm.makeMove(move)
                ns = GameState(self.gm.getGameState(), cs.depth + 1, move)
                if ns not in self.visited:
                    ns.parent = cs
                    cs.children.append(ns)
                self.gm.reverseMove(move)
            self.findNextStep()
        else:
            return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        cs = self.currentState
        self.visited[cs] = True

        # If already in correct state then return True
        if self.currentState.state == self.victoryCondition:
            return True

        moves = self.gm.getMovables()
        if not cs.children:
            if moves:  # Check if there is indeed moves
                for move in moves:
                    self.gm.makeMove(move)
                    ns = GameState(self.gm.getGameState(), cs.depth + 1, move)
                    if ns not in self.visited:
                        ns.parent = cs
                        cs.children.append(ns)
                        self.visited[ns] = False
                    self.gm.reverseMove(move)

        # Make our Queue
        queue = [self.currentState]

        while self.currentState in self.visited:
            self.currentState = queue.pop(0)
            # Queue new
            for children in self.currentState.children:
                queue.append(children)
                if children not in self.visited:
                    queue.append(children)
                    self.visited[children] = True

        next_state = self.currentState
        temp_state = next_state

        # now we need to get to the current state from the node
        path = []
        while temp_state.parent:
            path.insert(0, temp_state.requiredMovable)  # add to the path
            temp_state = temp_state.parent

        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        # now we make the moves
        for move in path:
            self.gm.makeMove(move)

        self.currentState = next_state
        if self.currentState == self.victoryCondition:
            return True
        else:
            return False
