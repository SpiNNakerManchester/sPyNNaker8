from builtins import print


class Step:
    """
    Represents a step taken by the agent.
    Contains the change in x and y coordinates and head direction
    """

    def __init__(self, change_x, change_y, head_dir):
        self.change_x = change_x
        self.change_y = change_y
        self.head_dir = head_dir

    def print_step(self):
        """
        Print the current step's details to console
        """
        print "Change in x coordinate: " + str(self.change_x) + "cm"
        print "Change in y coordinate: " + str(self.change_y) + "cm"
        print "Head direction: " + str(self.head_dir)
