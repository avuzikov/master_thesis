class ConnectivityComponent:
    def __init__(self, component_name):
        self._component_name = component_name
        self.BSs = []
    def getComponentName(self):
        return self._component_name
    def addBS(self, new_bs):
        self.BSs.append(new_bs)
    def __str__(self):
        # Generate a list of string representations of Point objects and join them with ', '
        bs_strings = [str(bs) for bs in self.BSs]
        component_str = "Connectivity Component: [" + ', '.join(bs_strings) + "]"
        return component_str
    __repr__ = __str__