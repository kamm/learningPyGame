import pygame
from tiles import Tile
from player import Player
from settings import tile_size, screen_width


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width * 0.2 and direction_x < 0:
            self.world_shift = player.base_speed
            player.speed = 0
        elif player_x > screen_width * 0.8 and direction_x > 0:
            self.world_shift = -1 * player.base_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player.base_speed

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.hitbox.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if player.direction.x < 0:
                    player.hitbox.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.hitbox.left
                    print(f"{player.on_left} {player.on_right} {player.on_ground}")

                elif player.direction.x > 0:
                    player.hitbox.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.hitbox.right

    def vertical_movement_collision(self):
        player = self.player.sprite

        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if player.direction.y < 0:
                    player.hitbox.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ground = False
                elif player.direction.y > 0:
                    player.hitbox.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_ground and (player.direction.y < 0 or player.direction.y > 1):
            player.on_ground = False

    def run(self):
        # tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
