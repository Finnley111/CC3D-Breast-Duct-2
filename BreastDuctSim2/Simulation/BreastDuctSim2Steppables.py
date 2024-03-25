from cc3d.core.PySteppables import *
import numpy as np
import random
import math



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        cellVol = 1000
        #this controls what each cell types' target volume will be
        #i.e how big it will grow before stoping
        for cell in self.cell_list:
            
            if cell.type != self.BOUND:
                cell.targetVolume = 25
                cell.lambdaVolume = 2.0
        
        
        cellWidth  =  7  # how wide one cell is (pixels)
        circleWidth= 100  # how wide the circle of cells is (pixels)
        numCells   =  48  # number of cells in the circle
        # center point of the CC3D window:
        xMid=self.dim.x/2 # these will change automatically if the model's size is changed
        yMid=self.dim.y/2
        
        # a list of the cell types that we are using for the circle, used to assign types 
        # to the cells in the circle. Must be the all uppercase verson of the cell type
        # names in the .xml file. You can omit types if you want.
        cellTypeList=["self.BOUND"]
            
        for iAng in range(numCells):  # iterate over number of cells to create
            ang=2*3.14159/numCells*iAng # rotation angle, radians
            # location of the center of this cell
            xCellCenter=int(xMid - circleWidth/2.*math.cos(ang))
            yCellCenter=int(yMid - circleWidth/2.*math.sin(ang))
            # create a new CC3D cell, the cell type is assigned from the list of cell 
            # types using iAng iterator as the index into the list
            newCell = self.new_cell(eval(cellTypeList[ iAng %len(cellTypeList)])) 
            # Iterate over all possible pixels for this cell
            for ix in range(xCellCenter-cellWidth, xCellCenter+cellWidth+1):
                for iy in range(yCellCenter-cellWidth, yCellCenter+cellWidth+1):
                    # use this pixel if it is close enough to the cell's center
                    if sqrt((ix-xCellCenter)**2+(iy-yCellCenter)**2) <= cellWidth/2:
                        #this actually assigns this pixel to this cell
                        self.cell_field[ix:ix+1, iy:iy+1, 0] = newCell
                
            # done with pixels for this cell, set its target colume
            newCell.targetVolume = newCell.volume
            newCell.lambdaVolume = 1000
        
        
        cellWidth  =  7  # how wide one cell is (pixels)
        circleWidth= 50  # how wide the circle of cells is (pixels)
        numCells   =  12  # number of cells in the circle
        # center point of the CC3D window:
        xMid=self.dim.x/2 # these will change automatically if the model's size is changed
        yMid=self.dim.y/2
        
        # a list of the cell types that we are using for the circle, used to assign types 
        # to the cells in the circle. Must be the all uppercase verson of the cell type
        # names in the .xml file. You can omit types if you want.
        cellTypeList=["self.EPI"]
            
        for iAng in range(numCells):  # iterate over number of cells to create
            ang=2*3.14159/numCells*iAng # rotation angle, radians
            # location of the center of this cell
            xCellCenter=int(xMid - circleWidth/2.*math.cos(ang))
            yCellCenter=int(yMid - circleWidth/2.*math.sin(ang))
            # create a new CC3D cell, the cell type is assigned from the list of cell 
            # types using iAng iterator as the index into the list
            newCell = self.new_cell(eval(cellTypeList[ iAng %len(cellTypeList)])) 
            # Iterate over all possible pixels for this cell
            for ix in range(xCellCenter-cellWidth, xCellCenter+cellWidth+1):
                for iy in range(yCellCenter-cellWidth, yCellCenter+cellWidth+1):
                    # use this pixel if it is close enough to the cell's center
                    if sqrt((ix-xCellCenter)**2+(iy-yCellCenter)**2) <= cellWidth/2:
                        #this actually assigns this pixel to this cell
                        self.cell_field[ix:ix+1, iy:iy+1, 0] = newCell
                
            # done with pixels for this cell, set its target colume
            newCell.targetVolume = 75
            newCell.lambdaVolume = 2.0
        
        
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
            elif mcs > 500 and field[cell.xCOM, cell.yCOM, 0]<50:
                    cell.type=self.NECR
                    
        #kill the necrotic cells
        for cell in self.cell_list_by_type(self.NECR):
            secretor.uptakeInsideCell(cell, 2.0, 0.01)
            if field[cell.xCOM, cell.yCOM, 0]<49:
                self.delete_cell(cell)
                
        for cell in self.cell_list_by_type(self.PROL):
            cellX = cell.xCOM
            cellY = cell.yCOM
            
            vecX = 0
            vecY = 0
            if (cell.xCOM > 150 and cell.xCOM < 200 and cell.yCOM > 100 and cell.yCOM < 150):
                vecX = cellX - 125
                vecY = cellY - 125
                print(cellX, " ",cellY)
                print(vecX, " ",vecY)
                cell.lambdaVecX = 5
                cell.lambdaVecY = 0
                cell.lambdaVecZ = 0
            
            
            
        
        # for cell in self.cell_list_by_type(self.LUM):
            # neighbor_list = self.get_cell_neighbor_data_list(cell)
            # neighbor_count_by_type_dict = neighbor_list.neighbor_count_by_type()
            
            # # if the neighbor is not the lumen, the chance for division is greater to make the simulation show more results
            # if 4 in neighbor_count_by_type_dict:
                # cell.targetVolume -= 1.5
        
        
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
            if cell.volume>60 and random.random() < 0.5 and cell.type != self.BOUND:
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

        