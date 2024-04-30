from cc3d import CompuCellSetup
        

from BreastDuctSim2Steppables import ConstraintInitializerSteppable
CompuCellSetup.register_steppable(steppable=ConstraintInitializerSteppable(frequency=1))


from BreastDuctSim2Steppables import GrowthSteppable
CompuCellSetup.register_steppable(steppable=GrowthSteppable(frequency=1))


from BreastDuctSim2Steppables import MitosisSteppable
CompuCellSetup.register_steppable(steppable=MitosisSteppable(frequency=1))

        
# JPS added
from BreastDuctSim2Steppables import Barrier_forcingSteppable
CompuCellSetup.register_steppable(steppable=Barrier_forcingSteppable(frequency=1))

CompuCellSetup.run()
