from cc3d.core.PySteppables import *
import numpy as np
import random



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        cellVol = 1000

        for cell in self.cell_list:

            cell.lambdaVolume = 10
            if cell.type == self.LUM:
                cell.targetVolume = .6*cellVol
            if cell.type == self.EPI:
                cell.targetVolume = .4*cellVol
        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        # secretor = self.get_field_secretor("Nutrients")
        # field = self.field.Nutrients

        for cell in self.cell_list_by_type(self.EPI):
            cell.targetVolume += 0.02      

        # for cell in self.cell_list_by_type(self.EPI): 
        #     secretor.uptakeInsideCell(cell, 2.0, 0.01) 
            
            # if field[cell.xCOM,cell.yCOM,0]>66:
            #     cell.type=self.PROL
        

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
        # DIVISION OF EPI CELLS
        for cell in self.cell_list_by_type(self.EPI):
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            
            # BEFORE 750 time steps the cells divide less frequently (helps control initial setup)
            if mcs < 750 and cell.volume>100 and random.random() < 0.01:
                cells_to_divide.append(cell)
            elif cell.volume>100 and random.random() < 0.1:
                cells_to_divide.append(cell)
            # if the neighbor is not the lumen, the chance for division is greater to make the simulation show more results
            elif 1 not in neighbor_count_by_type_dict:
                if cell.volume>25 and random.random() < 0.8:
                    cells_to_divide.append(cell)
                    
        for cell in cells_to_divide:

            # OTHER POSSIBLE WAYS TO DIVIDE CELLS
            # self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_minor_axis(cell)
            
           
            self.divide_cell_along_major_axis(cell)

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

        
class DeathSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        if mcs >= 800:
            i=0
            for i in range(5):
                for cell in self.cell_list:
                    if cell.type==1:
                        cell.targetVolume-=0.1
                        cell.lambdaVolume=100
                i+=1

        