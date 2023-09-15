import pygame as pg

from .helpers import directions_inv
from .vector2d import Vector2d

class Entity:
    def __init__(self, position: Vector2d, direction: Vector2d, dimension: Vector2d, speed: int):
        """
        Todas as entidates possuem esses três atributos.
        A posição representa topo direito da entidade.
        □° (ilustração)
        """
        self.position = position
        self.direction = direction
        self.dimension = dimension
        self.speed = speed
    
    def move(self):
        self.position = self.position + (self.direction * self.speed)

    def delete(self):
        """
        Para deletar uma entidade, deve-se também desreferenciar o objeto.
        Exemplo:
        >>> entity = Entity(v1, v2, v3)
        >>> entity.delete()
        >>> entity = None
        """
        self.position = None
        self.speed = None
        self.dimension = None

class Player(Entity):
    def __init__(
            self, 
            position: Vector2d, 
            direction: Vector2d, 
            dimension: Vector2d, 
            speed: int,
            stamina: int,
        ) -> None:
        super().__init__(position, direction, dimension, speed)
        self.position = position
        self.speed = speed
        self.dimension = dimension
        self.stamina = stamina
    
    def draw(self, screen):
        direction = directions_inv[self.direction]
        image = pg.image.load(f'assets/mago_{direction.lower()}.png')
        resized_img = pg.transform.smoothscale(image, self.dimension.val)
        screen.blit(resized_img, (self.position.val))
   



