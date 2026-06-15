# umm were gonna do a mix of 3d region nodes for collision and 2d sprites for visuals
import bascenev1 as bs
class Renderer:
    def __init__(self):
        self.actors: dict[
            bs.Node
        ] = {}
        self.camera_x = 0
        self.camera_y = 40
        bs.timer(0.011, self.update, repeat=True)
    def delete_all(self):
        for node in self.actors.values():
            node.delete()
        self.actors.clear()
        
    def register_actor(self, object, node):
        # register an actor so the object can edit and move around the node
        self.actors[object] = {
            'node': node,
            'position': (0, 0),
            'texture': None
        }

    def change_actor_position(self, object, position, texture):
        if object in self.actors:
            self.actors[object]['position'] = position
            self.actors[object]['texture'] = texture
            

    def update(self):
        for actor in self.actors.values():
            node = actor['node']
            position = actor['position']
            bs.animate_array(node, 'position', 2, {
                0: node.position,
                0.01: (
                    position + self.camera_x,
                    position + self.camera_y
                )
            })
            # should be already loaded
            node.texture = actor['texture']
            
        
class Fighter:
    preloaded = False
    # preload data.
    textures = {} # e.g ['texture1', 'texture2', ...]
    sounds = {} # e.g ['sound1', 'sound2', ...]
    meshes = {} # e.g ['mesh1', 'mesh2', ...]
    animations = {} # e.g {'idle': {'anim': [texture1, texture2, ...], 'speed': 0.1, 'loop': True}}

    # framedata
    
    weight = 1.0 # knockback rate
    speed = 1.0 # movement
    hurtbox = (50, 50) # size x and y

    def _preload(self):
        self.data = {
            'textures': {},
            'sounds': {},
            'meshes': {},
        }
        for texture in self.textures:
            self.data['textures'][texture].append(bs.gettexture(texture))
        for sound in self.sounds:   
            self.data['textures'][sound].append(bs.getsound(sound))
        for mesh in self.meshes:
            self.data['textures'][mesh].append(bs.getmesh(mesh))
        self.preloaded = True
        return self.data


    def __init__(self):
        pass
        # use create to spawn the fighter instance. this is used so it doesnt affect the entire Fighter class.
        # so do Fighter()._preload() in loading screens then Fighter().create()
        # this can also be used for leway to setup controls etc
        
    
    def create(self):
        if not self.preloaded:
            raise Exception("Preload data before creating a fighter")
        # 3D
        self.hurtbox = bs.newnode('region') # material shit later, and basically will handle collision
        self.position = (0, 0)
       

        # 2D
        self.texture = 
        self.renderer = Renderer() # gets renderer from activitiy


        # player
        self.controller = object # not a sessionplayer but a controller class thats assigned to a sessionplayer or CPU
        # unfortunate that bombsquad is super duper limited with contollers
        self.input_x = 0.0
        self.input_y = 0.0
        self.input_light = False
        self.input_medium = False
        self.input_heavy = False
        self.input_special = False

        self.hitstun_frames = 0


        self.facing_left =  True
        self.hitboxes = []
        bs.timer(0.1, self.tick, repeat=True)

    def tick(self):
        self.update_actor()

        if self.in_hitstun():
            for hitbox in self.hitboxes:
                hitbox.delete()
                self.hitboxes.clear()

    
    def create_hitbox(self, xoffs, yoffs, lasting: int = 10):
        material = None
        math = None# for offsets also do -xoffs if facing the other direction or smth
        hitbox = bs.newnode('region')
        self.hitboxes.append(hitbox)

        # frames until hitbox disappears
        bs.timer(0.16*lasting, hitbox.delete)

    def on_move_left_right(self, value):
        self.input_x = value
    def on_move_up_down(self, value):
        self.input_y = value
    def on_punch_press(self):
        self.input_light = True
    def on_punch_release(self):
        self.input_light = False
    def on_pickup_press(self):
        self.input_medium = True
    def on_pickup_release(self):
        self.input_medium = False
    def on_bomb_press(self):
        self.input_heavy = True
    def on_bomb_release(self):
        self.input_heavy = False
    def on_jump_press(self):
        self.input_special = True
    def on_jump_release(self):
        self.input_special = False
    

    
    def update_actor(self):
        # finds whatever our actor is and edits it
        self.renderer.change_actor_position(self, self.position)


    def in_hitstun(self):
        self.hitstun_frames = int(self.hitstun_frames)
        return self.hitstun_frames > 0
    def update_physics(self, ground_rect):
        # Apply movement based on state
        if self.moving_left: self.x_velocity -= 1.5
        if self.moving_right: self.x_velocity += 1.5
        
        # Apply Friction
        self.x_velocity *= 0.85
        self.rect.x += self.x_velocity

        # Handle Jump
        if self.wants_jump:
            if self.x_velocity > 0: self.x_velocity = -10
            else: self.x_velocity = 10
            self.vel_y = 15
            self.wants_jump = False # Reset jump after processing

        # Handle Gravity & Floor Collision
        self.vel_y -= 1
        self.rect.y -= self.vel_y
        
        if self.rect.colliderect(ground_rect):
            self.rect.y += self.vel_y
            self.vel_y = 0