import openmdao.api as om

class LandBOSSEComponent(om.ExplicitComponent):
    """
    This is a superclass for all the components that wrap LandBOSSE
    cost modules. It holds functionality used for the other components
    that wrap LandBOSSE cost modules.
    """

    def initialize(self):
        """
        There is one option for this component: verbosity. If it is
        set to true, the component will print the summary of costs
        with print() after it finishes calculating them.
        """
        self.options.declare('verbosity', default=True)
