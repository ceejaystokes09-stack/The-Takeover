from ursina import * 

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
