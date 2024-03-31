class ConnectivityComponent:
    def __init__(self):
        self.BSs = []
    def addBS(self, newBS):
        self.BSs.append(newBS)
    def __str__(self):
        # Generate a list of string representations of Point objects and join them with ', '
        bs_strings = [str(bs) for bs in self.BSs]
        component_str = "Connectivity Component: [" + ', '.join(bs_strings) + "]"
        return component_str
    __repr__ = __str__