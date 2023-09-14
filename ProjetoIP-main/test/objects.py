from vector import Vector2d

class Entity:
    def __init__(self, position: Vector2d, speed: Vector2d, dimension: Vector2d):
        """
        Todas as entidates possuem esses três atributos.
        A posição representa topo direito da entidade.
        □° (ilustração)
        """
        self.position = position
        self.speed = speed
        self.dimension = dimension
    
    def move(self):
        self.position += self.speed

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
