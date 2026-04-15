from ursina import * 

"""from typing import Dict, Tuple
import numpy as np

class bounding_boxes:
    boxes: Dict[str, np.ndarray] = {}

    def __init__(self, box_data: Dict[str, np.ndarray]):
        self.data = box_data
        self.add_global()

    def add_global(self):
        for name, data in self.data.items():
            bounding_boxes.boxes[name] = data

    @staticmethod
    def get_min_max(data: np.ndarray):
        min_vals = data.min(axis=0)
        max_vals = data.max(axis=0)
        return min_vals, max_vals

    @classmethod
    def check_box(cls, point: Tuple[int, int, int]):
        px, py, pz = point

        for name, data in cls.boxes.items():
            min_vals, max_vals = cls.get_min_max(data)

            if (min_vals[0] <= px <= max_vals[0] and
                min_vals[1] <= py <= max_vals[1] and
                min_vals[2] <= pz <= max_vals[2]):
                return name

        return None


bounding_boxes({f"box_{1}":np.array([(1,1,1),(-1,-1,-1)])})

bounding_boxes({f"box_{2}":np.array([(10,10,10),(8,8,8)])})

box: str = bounding_boxes.check_box((9,9,9))
print(box)

"""

#this version is a more updated version eg uses no function sand just uses numpy but it gives a different result so still dont know if im going to use
"""import numpy as np

bb = np.array([(1, 1, 1), (-1, -1, -1)])
diff = bb[0] - bb[1]
print(diff)""" 

"""from typing import Tuple, List


bounding_box_1:List[Tuple[int,int,int]] = [(1,1,1), (-1,-1,-1)]

def bounding_box_details(bounding_box:List[Tuple[int,int,int]])-> Tuple[float,float,float]:
    # cord1 = bounding_box[0]
    # cord2=bounding_box[1]
    
    # bx:float = cord1[0] - cord2[0]
    # by:float = cord1[1] - cord2[1]
    # bz:float = cord1[2] - cord2[2]
    # return(bx,by,bz)
    return (
        float(bounding_box[0][0] - bounding_box[1][0]),
        float(bounding_box[0][1] - bounding_box[1][1]),
        float(bounding_box[0][2] - bounding_box[1][2])
    )

print(bounding_box_details(bounding_box_1))"""
"""from typing import Dict, Tuple, Callable
from random import randint as ri
from time import perf_counter 

class Testing:
    target_positions: Dict[str, Tuple[int, int, int]] = {}
    def __init__(self, name: str):
        self.name = name
        self.generate_target_cords:Callable[[None], Tuple[int,int,int]] = lambda: (ri(-50,50), 0, ri(-50,50))
        self.target_cord: Tuple[int,int,int] = self.generate_target_cords()
        #self.check_other_targets()
        self.update_dict()
        
        #print(Testing.target_positions)
    def check_other_targets(self):
        # if len(Testing.target_positions) == 0:
        #     return
        for pos in Testing.target_positions.values():
            print("2")
            if self.target_cord == pos:
                self.target_cord = self.generate_target_cords()
                return self.check_other_targets()
    
    def update_dict(self):
        Testing.target_positions[self.name] = self.target_cord
        
        
start_time = perf_counter()
pos = (0,0,0)
suffix = "Dude_"
for i in range(10):
    Testing(f"{suffix}{i+1}")
print(Testing.target_positions)


end_time = perf_counter()

print(f"Execution time: {end_time - start_time:.6f} seconds")
"""

"""class Test:
    def __init__(self, target: int, current: int, grid: list[list[int]]):
        self.target_number = target # basically what number on the grid is the target value in this
        # scenario its 3
        self.current_number = current
        self.grid = grid
        self.visited: list[tuple[int,int]]=()
        self.target_pos, self.current_pos = self.search_grid()
        #self.calc_path()
    
    def search_grid(self):
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                if value == self.current_number:
                    print("Found current position at:", r, c)
                    cp = (r,c)
                if value == self.target_number:
                    print("Found target position at:", r, c)
                    tp = (r,c)
        
        return tp,cp
        
    
    #def calc_path(self):
        
    
grid = [
    [1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 3, 1],
    [1, 1, 1, 1, 1],
]

Test(3,2,grid)"""
