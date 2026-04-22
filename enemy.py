from ursina import *
from direct.actor.Actor import Actor  
#from panda3d.core import CollisionNode, CollisionBox, BitMask32

class Enemy(Entity):
    def __init__(self, model, player_ref, moving: bool = True ): # Pass the player object here
        super().__init__(scale=2.5, position=(20,0,20), color=color.red, wireframe=False)
        self.visual = Actor(model)
        self._model_ = model 
        self.visual.reparent_to(self)
        self.visual.loop("walking-no-gun")
        self.visual.setPlayRate(0.86, "walking-no-gun")
        #self.model=model
        self.wireframe = False
        self.clearRenderMode()

        self.visual.setRenderModeFilled()
        self.visual.clearRenderMode()
        self.visble=False

        
        # Physics & Jump Variables
        self.jump_height = 3
        self.velocity_y = 0
        self.gravity = 20
        self.grounded = False
        self.jumping = False 
        self.head_height = 4.7
        self.health: int | float = 250
        self.head_armour: bool = False
        self.Body_armour:bool = False

        # Movement & AI
        self.can_move = moving 
        self.speed = 12.42
        self.player = player_ref
        self.detection_range = 25 
        self.targetting_player = False 
        self.timer= 0 
        


        #self.create_range_visual()
        self.create_orb()
        self.create_hitboxes()
        
    def create_hitboxes(self):
        
        self.collider = CapsuleCollider(self, center=Vec3(0,0,0), height=3, radius=.45)#MeshCollider(self, self._model_, )
        #self.collision_model=self._model_



    def create_range_visual(self):
        # Scale is radius * 2 to cover the area correctly
        self.sphere = Entity(
            # model="sphere", 
            # scale=self.detection_range * 2, 
            # color=color.rgba(0, 255, 0, .350), 
            position=self.position,
            #double_sided = True
        )

    def target_player(self): 
        # Patrolling logic
        direction = (self.player.position- self.position).normalized()
        self.position += direction * time.dt * self.speed
        
        target_angle = math.degrees(math.atan2(direction.x, direction.z))
        self.rotation_y = lerp(self.rotation_y, target_angle + 180, 10 * time.dt)
        
        if distance(self.position, self.player.position) < 2:
            self.player.health -=10


    def check_player_in_range(self):
        # distance() returns a float, so we compare it to our float range
        dist = distance(self.world_position, self.player.world_position)
        if dist <= self.detection_range:
            #self.sphere.color = color.rgba(255, 0, 0, 50) # Red if close
            self.targetting_player = True 
            #print("Player in range!")
        # else:
        #     self.sphere.color = color.rgba(0, 255, 0, 50) # Green if far

    def create_orb(self):
        self.orb = Vec3(0,0,0)
        self.update_orb(Vec3(random.randint(-50,50), 0, random.randint(-50,50)))

    def update_orb(self, pos):
        if not self.targetting_player: 
            self.orb= pos


    def jump(self): 
        if self.jumping: 
            return 
        self.jumping = True 
        self.animate_y(self.y + self.jump_height, duration=0.25, curve=curve.out_quad) 
        invoke(self.jump_down, delay=0.25) 

    def jump_down(self): 
        self.animate_y(self.y - self.jump_height, duration=0.25, curve=curve.in_quad) 
        invoke(self.reset_jump, delay=0.25) 

    def reset_jump(self): 
        self.jumping = False 

    
    def die(self):
        self.targetting_player = False
        
        self.can_move = False
        
        # Animate a fall / collapse
        self.animate_rotation(Vec3(90, self.rotation_y, 0), duration=0.3, curve=curve.in_out_sine)
        self.animate_scale(self.scale * 1.05, duration=0.2, curve=curve.out_sine)  # slight squash for effect

        # Delay spawning the ragdoll a tiny bit
        invoke(self.spawn_ragdoll)#, delay=0.3)

        
        self.disable()

    def spawn_ragdoll(self):
        self.visible = False
        self.collider = None
        if hasattr(self, "visual"):
            self.visual.cleanup()
            self.visual.removeNode()
        
        ragdoll = Entity(
            model=self._model_,
            texture=getattr(self, 'texture', None),
            position=self.position,
            rotation=self.rotation,
            scale=self.scale,
            collider='box'
        )

        # Give it some physics
        ragdoll.velocity = Vec3(random.uniform(-4,4), random.uniform(3,6), random.uniform(-4,4))
        ragdoll.angular_velocity = Vec3(random.uniform(-200,200), random.uniform(-200,200), random.uniform(-200,200))
        ragdoll.gravity = 25
        ragdoll.drag = 0.98
        ragdoll.angular_drag = 0.95
        ragdoll.bounce = 0.3
        ragdoll.grounded = False

        def ragdoll_update():
            ragdoll.velocity.y -= ragdoll.gravity * time.dt
            ragdoll.velocity *= ragdoll.drag
            ragdoll.angular_velocity *= ragdoll.angular_drag
            ragdoll.position += ragdoll.velocity * time.dt
            ragdoll.rotation += ragdoll.angular_velocity * time.dt

            # Ground collision
            ground_hit = raycast(ragdoll.world_position + Vec3(0,2,0), Vec3(0,-1,0), distance=5, ignore=(ragdoll,))
            if ground_hit.hit:
                if ragdoll.y <= ground_hit.world_point.y:
                    ragdoll.y = ground_hit.world_point.y
                    if abs(ragdoll.velocity.y) > 1:
                        ragdoll.velocity.y *= -ragdoll.bounce
                    else:
                        ragdoll.velocity.y = 0
                    ragdoll.velocity.x *= 0.6
                    ragdoll.velocity.z *= 0.6
                    ragdoll.angular_velocity *= 0.5
                    ragdoll.grounded = True

            # Stop when settled
            if ragdoll.grounded and ragdoll.velocity.length() < 0.1 and ragdoll.angular_velocity.length() < 5:
                ragdoll.velocity = Vec3(0,0,0)
                ragdoll.angular_velocity = Vec3(0,0,0)
                ragdoll.animate_rotation(Vec3(90, ragdoll.rotation_y, 0), duration=0.3)
                ragdoll.update = self.despawn_ragdoll

        ragdoll.update = ragdoll_update
    def despawn_ragdoll(self):
        self.timer += time.dt
        if self.timer >= 3: destroy(self)
    def update(self):
        if self.health <= 0:
            if self.enabled:
                self.die()
            return

        if not self.can_move:
            return
        # Keep the visual sphere attached to the enemy
        #self.sphere.position = self.position 
        
        # Run the detection check
        self.check_player_in_range()
        if not self.targetting_player:
            # Patrolling logic
            direction = (self.orb- self.position).normalized()
            self.position += direction * time.dt * self.speed
            
            target_angle = math.degrees(math.atan2(direction.x, direction.z))
            self.rotation_y = lerp(self.rotation_y, target_angle + 180, 10 * time.dt)
            
            if distance(self.position, self.player.position) < 1: 
                self.player.health -= 10 

            if distance(self.position, self.orb) < 1:
                pos = Vec3(random.randint(-50,50), 0, random.randint(-50,50))
                self.update_orb(pos)       
        else: self.target_player() 










# def spawn_ragdoll_with_bones(self, enemy_entity, bone_names_list):
    #     """
    #     enemy_entity: the Enemy Entity to turn into ragdoll
    #     bone_names_list: list of bone names in the .glb armature you want to animate
    #     """
        
    #     # Hide the original enemy
    #     enemy_entity.enabled = False
    #     enemy_entity.visible = False
    #     enemy_entity.collider = None

    #     # Create the ragdoll entity
    #     ragdoll = Entity(
    #         model=enemy_entity.model,
    #         texture=getattr(enemy_entity, 'texture', None),
    #         position=enemy_entity.position,
    #         rotation=enemy_entity.rotation,
    #         scale=enemy_entity.scale,
    #         collider='box'
    #     )

    #     # Physics parameters
    #     ragdoll.velocity = Vec3(random.uniform(-4,4), random.uniform(3,6), random.uniform(-4,4))
    #     ragdoll.angular_velocity = Vec3(random.uniform(-200,200), random.uniform(-200,200), random.uniform(-200,200))
    #     ragdoll.gravity = 25
    #     ragdoll.drag = 0.98
    #     ragdoll.angular_drag = 0.95
    #     ragdoll.bounce = 0.3
    #     ragdoll.grounded = False

    #     # Grab bones from the model for flailing
    #     ragdoll.bones_to_flail = []
    #     for name in bone_names_list:
    #         if name in ragdoll.model.bones:
    #             ragdoll.bones_to_flail.append(ragdoll.model.bones[name])
    #         else:
    #             print(f"[WARNING] Bone '{name}' not found in model!")

    #     # Update function for physics + bone flail
    #     def ragdoll_update():
    #         # Apply gravity
    #         ragdoll.velocity.y -= ragdoll.gravity * time.dt

    #         # Apply drag
    #         ragdoll.velocity *= ragdoll.drag
    #         ragdoll.angular_velocity *= ragdoll.angular_drag

    #         # Move + rotate
    #         ragdoll.position += ragdoll.velocity * time.dt
    #         ragdoll.rotation += ragdoll.angular_velocity * time.dt

    #         # Ground collision
    #         ground_hit = raycast(ragdoll.world_position + Vec3(0,2,0), Vec3(0,-1,0), distance=5, ignore=(ragdoll,))
    #         if ground_hit.hit:
    #             if ragdoll.y <= ground_hit.world_point.y:
    #                 ragdoll.y = ground_hit.world_point.y
    #                 if abs(ragdoll.velocity.y) > 1:
    #                     ragdoll.velocity.y *= -ragdoll.bounce
    #                 else:
    #                     ragdoll.velocity.y = 0
    #                 ragdoll.velocity.x *= 0.6
    #                 ragdoll.velocity.z *= 0.6
    #                 ragdoll.angular_velocity *= 0.5
    #                 ragdoll.grounded = True

    #         # Flail the bones
    #         for bone in ragdoll.bones_to_flail:
    #             bone.rotation += Vec3(
    #                 random.uniform(-120,120) * time.dt,
    #                 random.uniform(-120,120) * time.dt,
    #                 random.uniform(-120,120) * time.dt
    #             )

    #         # Stop condition when settled
    #         if ragdoll.grounded and ragdoll.velocity.length() < 0.1 and ragdoll.angular_velocity.length() < 5:
    #             ragdoll.velocity = Vec3(0,0,0)
    #             ragdoll.angular_velocity = Vec3(0,0,0)
    #             ragdoll.update = None
    #             # Optional: lay flat
    #             ragdoll.animate_rotation(Vec3(90, ragdoll.rotation_y, 0), duration=0.3)

    #     ragdoll.update = ragdoll_update


    # # 1. BODY HITBOX
        # # We create a CollisionNode specifically for the body
        # body_cnode = CollisionNode('Enemy_Body')
        
        # # CollisionBox arguments: (CenterPoint, x_half_width, y_half_depth, z_half_height)
        # # Assuming your enemy is roughly 2 units tall, center it at z=1
        # body_shape = CollisionBox((0, .87, 0), .4, .85, .4)
        # body_cnode.addSolid(body_shape)
        
        # # Set masks (Bit 1 for bullets)
        # body_cnode.setIntoCollideMask(BitMask32.bit(1))
        # body_cnode.setFromCollideMask(BitMask32.allOff())
        
        # # Attach to 'self' so it moves with the Enemy
        # self.body_path = self.attachNewNode(body_cnode)
        # self.body_path.setPythonTag("Enemy", self) # Tag the path so Bullet can find 'self'
        
        # # 2. HEAD HITBOX (For Crits)
        # head_cnode = CollisionNode('Enemy_Head')
        # # Place the sphere at the head height (e.g., z=2.2)
        # head_shape = CollisionSphere(0, 1.1, 0, 0.3) 
        # head_cnode.addSolid(head_shape)
        
        # head_cnode.setIntoCollideMask(BitMask32.bit(1))
        # head_cnode.setFromCollideMask(BitMask32.allOff())
        
        # self.head_path = self.attachNewNode(head_cnode)
        # self.head_path.setPythonTag("Enemy", self)
        # self.head_path.setPythonTag("is_headshot", True) # Extra tag for logic

        # # DEBUG: Essential to see if it's moving!
        # self.body_path.show() 
        # self.head_path.show()


        # cnode = CollisionNode('Enemy')
        # cnode.addSolid(CollisionBox((0,1,0), 0.5,1,0.5))

        # cnode.setIntoCollideMask(BitMask32.bit(1))
        # cnode.setFromCollideMask(BitMask32.allOff())

        # self.cnode_path = self.attachNewNode(cnode)
        # self.cnode_path.show()
        # self.setPythonTag("Enemy", self)

        # self.cnode_path = self.visual.attachNewNode(cnode)
        # #self.cTrav.showCollisions(render)
        # self.cnode_path.show()
