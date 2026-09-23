import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroid_field import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)    
    asteroid_field_obj = AsteroidField()

    Shot.containers = (shots, drawable, updatable)

    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for item in drawable:
            item.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        for item in updatable:
            item.update(dt)
        
        for item in asteroids:
            collided = item.collides_with(player)
            if collided == True:
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            for shot_item in shots:
                hit_asteroid = shot_item.collides_with(item)
                if hit_asteroid == True:
                    log_event("asteroid_shot")
                    shot_item.kill()
                    item.split()
        


if __name__ == "__main__":
    main()
