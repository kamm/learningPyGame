import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 1/10
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0,0)

        # player movement
        self.walk_speed = 5
        self.run_speed = 8
        self.base_speed = self.walk_speed
        self.speed = self.base_speed
        self.gravity = 0.8
        self.jump_speed = -16
        self.hitbox = pygame.Rect(self.rect.topleft, (47, self.rect.height))
        self.status = 'idle'

        self.facing_right = True
        self.on_ground = True
        self.on_left = True
        self.on_right = True

    def import_character_assets(self):
        character_path = 'assets/graphics/character/'
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        pygame.draw.rect(image, 'red', (0, 0, self.hitbox.width, self.hitbox.height), 1)
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.hitbox.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.rect.bottomright = self.hitbox.bottomright
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.base_speed = self.run_speed
            print("run")
        else:
            self.base_speed = self.walk_speed
            print("walk")

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x == 0:
                self.status = 'idle'
            else:
                self.status = 'run'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.hitbox.y += self.direction.y

    def is_on_ground(self):
        return self.on_ground

    def jump(self):
        if self.is_on_ground():
            self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
