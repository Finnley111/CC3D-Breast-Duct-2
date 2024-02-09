from cc3d.core.PySteppables import *
import numpy as np



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        cellVol = 1000
        #this controls what each cell types' target volume will be
        #i.e how big it will grow before stoping
        for cell in self.cell_list:
            
            cell.lambdaVolume = 10
            if cell.type == self.LUM:
                cell.targetVolume = .6*cellVol
            else:
                cell.targetVolume = 25
                cell.lambdaVolume = 2.0
        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
    
        secretor = self.get_field_secretor("Nutrients")
        field = self.field.Nutrients
        
        
        
    
        # implements the uptake of the cells
        for cell in self.cell_list_by_type(self.PROL):
            cell_secr = secretor.uptakeInsideCellTotalCount(cell, 2.0, 0.01) # calculates total amount of nutrients that is uptaken
            cell.targetVolume += -cell_secr.tot_amount/100
                
            #if cells do not have enough uptake, they become QUIE
            if field[cell.xCOM, cell.yCOM, 0]<66:
                cell.type=self.QUIE
        
        for cell in self.cell_list_by_type(self.QUIE):
            # arguments are: cell, max uptake, relative uptake
            secretor.uptakeInsideCell(cell, 2.0, 0.01)
            
            if field[cell.xCOM, cell.yCOM, 0]>66:
                    cell.type=self.PROL
            elif mcs > 500 and field[cell.xCOM, cell.yCOM, 0]<10:
                    cell.type=self.NECR
                    
        #kill the necrotic cells
        for cell in self.cell_list_by_type(self.NECR):
            cell.targetVolume -= 1
        
        for cell in self.cell_list_by_type(self.LUM):
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            
            # if the neighbor is not the lumen, the chance for division is greater to make the simulation show more results
            if 4 in neighbor_count_by_type_dict:
                cell.targetVolume -= 1.5
        
        
        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        # field = self.field.CHEMICAL_FIELD_NAME
        
        # for cell in self.cell_list:
            # concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

            # # you can use here any fcn of concentrationAtCOM
            # cell.targetVolume += 0.01 * concentrationAtCOM       

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list:
            if cell.volume>50 and cell.type != self.LUM:
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        # if self.parent_cell.type==1:
            # self.child_cell.type=2
        # else:
            # self.child_cell.type=1

        