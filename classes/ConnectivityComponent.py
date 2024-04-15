class ConnectivityComponent:
    def __init__(self):
        self.BSs = []
    def addBS(self, new_bs):
        self.BSs.append(new_bs)
    def __str__(self):
        # Generate a list of string representations of Point objects and join them with ', '
        bs_strings = [str(bs) for bs in self.BSs]
        component_str = "Connectivity Component: [" + ', '.join(bs_strings) + "]"
        return component_str
    __repr__ = __str__