from cc3d import CompuCellSetup
        

from BreastDuck_withPushSteppables import ConstraintInitializerSteppable
CompuCellSetup.register_steppable(steppable=ConstraintInitializerSteppable(frequency=1))


from BreastDuck_withPushSteppables import GrowthSteppable
CompuCellSetup.register_steppable(steppable=GrowthSteppable(frequency=1))


from BreastDuck_withPushSteppables import MitosisSteppable
CompuCellSetup.register_steppable(steppable=MitosisSteppable(frequency=1))

        
# JPS added
from BreastDuck_withPushSteppables import Barrier_forcingSteppable
CompuCellSetup.register_steppable(steppable=Barrier_forcingSteppable(frequency=1))

CompuCellSetup.run()
