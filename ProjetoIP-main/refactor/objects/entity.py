import pygame as pg

from .helpers import directions_inv
from .vector2d import Vector2d

class Entity:
    def __init__(
            self, 
            position: Vector2d, 
            direction: Vector2d, 
            dimension: Vector2d, 
            speed: int, 
            image: bytearray):
        """
        Todas as entidates possuem esses três atributos.
        A posição representa topo direito da entidade.
        □° (ilustração)
        """
        self.position = position
        self.direction = direction
        self.dimension = dimension
        self.speed = speed
        self.image = image
    
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
            image: bytearray,
        ) -> None:
        super().__init__(position, direction, dimension, speed, image)
        self.position = position
        self.speed = speed
        self.dimension = dimension
        self.stamina = stamina
    
    def draw(self, screen):
        direction = directions_inv[self.direction]
        image = pg.image.load(f'assets/mago_{direction.lower()}.png')
        resized_img = pg.transform.smoothscale(image, self.dimension.val)
        screen.blit(resized_img, (self.position.val))

class Animal(Entity):
    def __init__(
            self, 
            position: Vector2d, 
            direction: Vector2d, 
            dimension: Vector2d, 
            speed: int,
            image: bytearray,
        ) -> None:
        super().__init__(position, direction, dimension, speed, image)
        self.position = position
        self.speed = speed
        self.dimension = dimension
    
    def move(self):
        """
        Movimentação deve ser aleatória
        """
        raise NotImplementedError
    
    def draw(self, screen):
        raise NotImplementedError
        direction = directions_inv[self.direction]
        image = pg.image.load(f'assets/mago_{direction.lower()}.png')
        resized_img = pg.transform.smoothscale(image, self.dimension.val)
        screen.blit(resized_img, (self.position.val))

class Tiles(Entity):
    def __init__(
            self, 
            position: Vector2d, 
            direction: Vector2d, 
            dimension: Vector2d, 
            speed: int,
            image: bytearray,
            ):
        super().__init__(position, direction, dimension, speed, image)

class Wall(Entity):
    def __init__(
        self, 
        position: Vector2d, 
        direction: Vector2d, 
        dimension: Vector2d, 
        speed: int,
        image: bytearray,
        ):
        super().__init__(position, direction, dimension, speed, image)

class Group:
    """
    Esta classe é usada para agrupar instâncias de Entity
    """
    def __init__(self):
        self.items = []
    
    def add(self, item: Entity) -> None:
        self.items.append(item)
    
    def remove(self, item: Entity) -> None:
        self.items.pop(item)
    
    def belongs(self, item: Entity) -> bool:
        return item in self.items
    
    def destroy(self):
        self.items = None
    


   



