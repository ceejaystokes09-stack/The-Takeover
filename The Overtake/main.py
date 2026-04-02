from ursina import *
#import math as m  #needed for character rotations 

app = Ursina()


class DebugCamera(Entity):
    def __init__(self):
        super().__init__()
        self.move_speed = 25
        self.can_move =True 

        camera.parent = self
        camera.position = (50,50,50)
        self.position = camera.position
        self.console()
        #TODO: need to add a way to teleport to any entity in the scene to make finding them and debugging easier


    def console(self):

        self.p_txt = Text(text=f"{self.position = } \n {camera.position= }",
                          scale = 2,
                          parent=camera.ui,
                          position=(-0.5, 0.45,-10))
        self.m_s_txt = Text(text=f"{self.move_speed = }",
                            scale = 2,
                            parent=camera.ui,
                            position=(-0.5, 0.35,-10))
        self.r_txt = Text(text=f"{self.rotation = }",
                            scale = 2,
                            parent=camera.ui,
                            position=(-0.5, 0.25,-10))

    def update(self):
        if not self.can_move:
            return
        
        if held_keys["left mouse"]:
            self.rotation_y += mouse.velocity[0] * 100
            self.rotation_x -= mouse.velocity[1] * 100
            self.rotation_x = clamp(self.rotation_x, -90, 90)

        movement = Vec3(
            held_keys["d"] - held_keys["a"],
            held_keys["space"] - held_keys["left shift"],
            held_keys["w"] - held_keys["s"]
        )

        self.position += (
            self.forward * movement.z +
            self.right * movement.x +
            self.up * movement.y
        ) * self.move_speed * time.dt

        self.move_speed = max(10, min(50, self.move_speed))

        self.p_txt.text=f"{self.position = } \n {camera.position= }"
        self.m_s_txt.text=f"{self.move_speed = }"
        self.r_txt.text=f"{self.rotation = }"
        

    def input(self, key):
        if key == "o":
            self.move_speed += 10
        if key == "u":
            self.move_speed -= 10


class ThirdPersonCamera(Entity):
    def __init__(self, player):
        super().__init__()
        self.player = player

        self.distance = 23.43
        self.height = 3.925
        self.rotation_speed = 100

        self.rotation_x = 4.35
        self.rotation_y = 180

        camera.parent = self
        camera.position = (0, self.height, -self.distance)  # OFFSET HERE

    def update(self):
        # Follow player position
        self.position = self.player.position

        # Mouse rotation
        # if held_keys["right mouse"]: 
        #     self.rotation_y += mouse.velocity[0] * self.rotation_speed
        #     self.rotation_x -= mouse.velocity[1] * self.rotation_speed
        #     self.rotation_x = clamp(self.rotation_x, -30, 60)
        self.rotation_y += mouse.velocity[0] * self.rotation_speed
        self.rotation_x -= mouse.velocity[1] * self.rotation_speed
        self.rotation_x = clamp(self.rotation_x, -30, 60)

        # Apply rotation to the rig
        self.rotation = (self.rotation_x, self.rotation_y, 0)       

class FirstPersonCamera(Entity):
    def __init__(self, player):
        super().__init__()
        self.player = player

        camera.parent = self
        camera.posion = self.position 

    def update(self):
        self.position = self.player.position

        # Mouse rotation
        # if held_keys["right mouse"]:
        #     self.rotation_y += mouse.velocity[0] * self.rotation_speed
        #     self.rotation_x -= mouse.velocity[1] * self.rotation_speed
        #     self.rotation_x = clamp(self.rotation_x, -30, 60)
        self.rotation_y += mouse.velocity[0] * self.rotation_speed
        self.rotation_x -= mouse.velocity[1] * self.rotation_speed
        self.rotation_x = clamp(self.rotation_x, -30, 60)

        # Apply rotation to the rig
        self.rotation = (self.rotation_x, self.rotation_y, 0) 



class Player(Entity):
    def __init__(self, model):
        super().__init__(model=model, collider='box',scale=.8)#rotation=(0,180,0))
        self.move_speed = 12
        self.can_move = True
        self.jump_height = 2 
        self.gravity = 20
        self.velocity_y = 0
        self.grounded = True

    def jump_down(self):
        self.animate_position((self.position[0], self.position[1] - self.jump_height), 0.25)
        if self.position[1] < 0: self.position[1] = 0 

    #@after(.35)
    def jump(self):
        if getattr(self, "jumping", False):
            return

        self.jumping = True

        self.animate_y(self.y + self.jump_height, duration=0.25)
        invoke(self.jump_down, delay=0.25)


    def jump_down(self):
        self.animate_y(0, duration=0.25)
        invoke(self.reset_jump, delay=0.25)


    def reset_jump(self):
        self.jumping = False


    def input(self, key):
        if key =="space": self.jump()    

    def update(self):
        if not self.can_move:
            return 

        self.velocity_y -= self.gravity * time.dt
        self.y += self.velocity_y * time.dt


        if self.y <= 0:
            self.y = 0
            self.velocity_y = 0
            self.grounded = True
        

        movement = Vec3(
            held_keys["d"] - held_keys["a"],
            0,
            held_keys["w"] - held_keys["s"]
        )

        self.rotation_y = lerp(self.rotation_y, camera.world_rotation_y + 180, 10 * time.dt)
        if movement.length() > 0:
            movement = movement.normalized() 

            cam_forward = Vec3(camera.forward.x, 0, camera.forward.z).normalized() 
            cam_right = Vec3(camera.right.x, 0, camera.right.z).normalized()

            move_dir = cam_forward * movement.z + cam_right * movement.x 

            self.position += move_dir * self.move_speed * time.dt
#hi

class Enemy(Entity):
    def __init__(self, model):
        super().__init__(model=model, scale=.8, position=(10,0,10), color=color.red)

        self.speed = 3
        self.create_orb()

    def create_orb(self):
        self.orb = Entity(model="cube", scale=.5, color=color.cyan)
        self.update_orb(Vec3(random.randint(0,50), 0, random.randint(0,50)))

    def update_orb(self, pos):
        self.orb.position = pos

    def update(self):

        direction = (self.orb.position - self.position).normalized()
        self.position += direction * time.dt * self.speed
        target_angle = math.degrees(math.atan2(direction.x, direction.z))
        self.rotation_y = lerp(self.rotation_y, target_angle + 180, 10 * time.dt)
        if distance(self.position, self.orb.position) < 1:
            pos = Vec3(random.randint(0,50), 0, random.randint(0,50))
            self.update_orb(pos)
        
class Throwable(Entity):
    def __init__(self, dmg: int | float = 0 , Dmg_radius: Vec3 = (0,0,0), distraction_radius: Vec3 = (0,0,0), distracts: bool = False,
    mass: int | float = 0, force: Vec3 = (0,0,0), Velocity: Vec3 = (0,0,0), Gravity: int | float = 9.8  ):
        super().__init__()
        self.damage = dmg    
        self.dmg_rnge = Dmg_radius
        self.distraction_range = distraction_radius
        self.distracts_enemies = distracts 
        self.mass = mass 
        self.force = force
        self.Velocity = velocity 
        self.gravity = Gravity # used real world gravity for kwarg so it can try to match real world physics, may change soon though 

    def throw(self):
        pass 
        """we want the force of the player with and the projectory of the throw to calulate the distance it travles, 
        spped and velocity to then calculate any drag, momentum or even bounce of the throwable"""    
    def show_trail_line(self): 
        pass 
        """I will make a visual represntation of the throw of the grenade using whitel line so player knows where there aiming
        might chnage this in the future to just make the user have to aim with cursor and then will have to gess how high up, not yet decide 
        tho"""

    def update(self):
        acceleration = self.force / self.mass
        self.Velocity += acceleration * time.dt
        self.position += self.Velocity * time.dt


        """dont know if this needed yet, probably though to actually calultae the momentum or stuff, dont yet know what to do, kind of just brain 
        storming at the moment, """

sky = Sky()
ground = Entity(model='plane',texture="grass", scale=250, collider='box', color=color.green)

player = Player("assets/Characters.glb")

Enemy = Enemy("assets/Characters.glb")

debug_cam = DebugCamera()
third_cam = ThirdPersonCamera(player)



mode = "third"
debug_cam.disable()
mouse.visible = False
mouse.locked = True

def input(key):
    global mode
    if key == "escape":
        quit()
    if key == "tab":
        if mode == "third":
            third_cam.disable()
            player.can_move = False
            debug_cam.enable()
            debug_cam.can_move = True

            camera.parent = debug_cam
            mode = "debug"
            mouse.visible = True
            mouse.locked = False

        else:
            debug_cam.disable()
            player.can_move = True
            third_cam.enable()
            debug_cam.can_move = False 

            camera.parent = third_cam
            mode = "third"  
            mouse.visible = False
            mouse.locked = True



app.run()
