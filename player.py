from ursina import * 
from Scripts.Weapons import shootable, Melee



class Player(Entity):
    Pos:Vec3 = Vec3(0,0,0)
    def __init__(self, model):
        super().__init__(model=model, collider='box', scale=.8, name="player", camera_ref= None)
        self.position=(100,5,100)
        self.move_speed = 12
        self.can_move = True
        self.jump_height = 3
        self.velocity_y = 0
        self.weapons = {"Mp5": shootable("assets/mp5_black.glb", player_ref=self, attack_dmg=63),
                        "stick": Melee(self),
                        }
        self.equipped = "Mp5"
        self.change_weapon()
        
        self.gravity = 20
        self.grounded = True
        self.jumping = False 
        self.max_health = 100
        self.health = self.max_health  # Current health
        # self.has_weapon = True
        # self.weapon = weapon 
    
    def change_weapon(self):
        for weapon_name, e in self.weapons.items():
            if weapon_name == self.equipped:
                self.weapons[weapon_name].enable()
            self.weapons[weapon_name].disable

    def jump(self): 
        if self.jumping or not self.grounded: 
            return 
        self.jumping = True 
        self.animate_y(self.y + self.jump_height, duration=0.25, curve=curve.out_quad) 
        invoke(self.jump_down, delay=0.25) 

    def jump_down(self): 
        # We animate down, but gravity will take over once reset_jump is called
        self.animate_y(self.y - self.jump_height, duration=0.25, curve=curve.in_quad) 
        invoke(self.reset_jump, delay=0.25) 

    def reset_jump(self): 
        self.jumping = False 

    def input(self, key): 
        if key == "space" and self.can_move: 
            self.jump()

        if key == "1":
            self.equipped = "Mp5"
            self.change_weapon()
        if key == "2":
            self.equipped = "stick"
            self.change_weapon()
        #if key == ".": self.health -= 10 

    def update(self):
        if not self.can_move:
            return

        # --- GRAVITY & GROUND COLLISION ---
        if not self.jumping:
            self.velocity_y -= self.gravity * time.dt
            self.y += self.velocity_y * time.dt

            
            # 'debug=True' lets you see a yellow line in the scene showing the ray
            ground_hit = raycast(self.world_position + Vec3(0, 1, 0), Vec3(0, -1, 0), 
                                 distance=1, ignore=(self,), debug=True)
            
            if ground_hit.hit:
                self.grounded = True
                self.velocity_y = 0
                self.y = ground_hit.world_point.y
            else:
                self.grounded = False


        movement = Vec3(
            held_keys["d"] - held_keys["a"],
            0,
            held_keys["w"] - held_keys["s"]
        )

        if movement.length() > 0:
            movement = movement.normalized()
            cam_forward = Vec3(camera.forward.x, 0, camera.forward.z).normalized()
            cam_right = Vec3(camera.right.x, 0, camera.right.z).normalized()
            move_dir = cam_forward * movement.z + cam_right * movement.x

            # Wall collision check
            hit = raycast(self.world_position + Vec3(0, 0.5, 0), move_dir, 
                          distance=1, ignore=(self,))
            
            if not hit.hit:
                self.position += move_dir * self.move_speed * time.dt

            self.rotation_y = lerp(self.rotation_y, camera.world_rotation_y + 180, 10 * time.dt)
            Player.Pos = self.position 


class HealthBar(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        

        self.bg = Entity(parent=self, model='quad', color=color.dark_gray, scale=(0.3,0.03), z=0)
        

        self.bar = Entity(parent=self, model='quad', color=color.lime, scale=(0.3,0.03), z=-0.001)
        
        # Position on screen
        self.position = (-0.65, -.3745)
    
    def update(self):
        # Scale the green bar relative to health
        health_ratio = max(0, self.player.health / self.player.max_health)
        self.bar.scale_x = 0.3 * health_ratio
        if self.player.health <= 0:
            self.bar.scale_x = 0 
