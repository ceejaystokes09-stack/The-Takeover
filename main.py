from ursina import *
from player import Player, HealthBar 
from enemy import Enemy 
from Scripts.Cameras import FirstPersonCamera
from Scripts.Weapons import shootable, Melee 
from Debuging import DebugCamera
#import py
#from ursina.prefabs.first_person_controller import FirstPersonController as FPC 


# def disable_guns():
#         for i in weapons:
#             i.disable()
# def reanable_weapons():
#     for i in weapons:
#         i.enable()

def input(key):
        global mode
        # if key == "1":
        #      enemy.hitbox.hide() 
        # if key == "2": enemy.hitbox.show()
        if key == "escape":
            quit()
        if key == "tab":
            if mode == "third":
                third_cam.disable()
                player.can_move = False
                debug_cam.enable()
                debug_cam.can_move = True
                #disable_guns()

                camera.parent = debug_cam
                mode = "debug"
                mouse.visible = True
                mouse.locked = False

            

            else:
                debug_cam.disable()
                player.can_move = True
                third_cam.enable()
                debug_cam.can_move = False 
                #reanable_weapons()
                camera.parent = third_cam
                mode = "third"  
                mouse.visible = False
                mouse.locked = True
if __name__ == "__main__":
    app = Ursina()
        





    sky = Sky()
    ground = Entity(model='plane',texture="grass", scale=250, collider='box', color=color.green)

    #stairs = generate_stairs(position=(20,20,20))
    #stairs.generate_normals()
    player = Player("cube")#"assets/Characters.glb")
    player.y = 10
    player_health_ui = HealthBar(player)
    for i in range(5):#random.randint(1, 100)):
        enemy = Enemy("assets/Characters.glb", player)

    debug_cam = DebugCamera()#enemy)
    third_cam = FirstPersonCamera(player)#ThirdPersonCamera(player)
    #first = FirstPersonCamera(player)
    #stick = Melee(player, third_cam).disable()
    #gun = shootable("assets/mp5_black.glb", player_ref=player, Camera=third_cam, attack_dmg=63)
    mode = "third"
    debug_cam.disable()
    mouse.visible = False
    mouse.locked = True
    #wall= Entity(model="Plane", rotation=(90,0,0), scale=20, color=color.red, double_sided=True)
    #weapons =  [gun]
    #print(pi)
    
    





    app.run()