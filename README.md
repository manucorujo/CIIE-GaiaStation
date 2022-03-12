# CIIE-GaiaStation

## Bugs

 * Bala: al chocar con una pared del lado izquiero el comportamiento de la colisión no es el deseado, problemas con el rect.
## Resource Manager

Tenemos tres funciones para cargar datos:

 * LoadImage: cargamos una imagen tal cual, por ejemplo la de fondo (carpeta Image)
 * LoadSprite: es como la anterior pero con la utilidad de colorKey para borrar el fondo (carpeta Sprite)
 * LoadLevelDefinitionFile: carga el archivo de definición de un nivel (carpeta levels)
 * CargarArchivoCoordenadas: carga un archivo de coordenadas de un sprite sheet determinado (carpeta Sprites)

## Sprites

En la carpeta uml se incluye el UML actual con todas las clases correspondientes a los Sprites, 
además del dichero .drawio para poder editarlo en la correspondiente plataforma.

Sprites originales: https://mattwalkden.itch.io/free-robot-warfare-pack

¿Por qué tienen una función get_image?

Para así en la función custom_draw de level.py, cuando se vaya a dibujar cada elemento se use, en vez de llamar al atributo 
image de cada objeto. Pero además de esta regla del software, conseguimos que para cada postura de un personaje se puede mostrar
una imagen distinta, por tanto el get_image de cada personaje es más complejo que el de un obstaculo, que solo devolverá el atributo imagen

## Patrones de diseño

En esta sección se apuntarán los patrones de diseño recomendados por el profesor y alguno adicional que utilicemos.
Además se debería incluir en que sección lo utilizamos, para la realización de la memoria o comentarios en el código.

### Observer

Define una dependencia del tipo uno a muchos entre objetos, de manera que cuando uno de los objetos cambia su estado, notifica este cambio a todos los dependientes.

### Singletone

Se asegura de que solo exista una única instancia del objeto y proporciona un acceso global a esta. Ejemplos: Gestor de recursos.

### Decorator

Este patrón de diseño de software nos proporciona una forma fácil de añadir responsabilidades adicionales a un objeto de forma dinámica y sin tener que modificar este objeto. Además proporciona una alternativa a la herencia para extender su funcionalidad.

### Inyección de dependencias

De esta no estoy tan seguro. Se suministran objetos a una clase en lugar de ser la propia clase la que cree dichos objetos. Esos objetos cumplen contratos que necesitan nuestras clases para poder funcionar (de ahí el concepto de dependencia). Nuestras clases no crean los objetos que necesitan, sino que se los suministra otra clase 'contenedora' que inyectará la implementación deseada a nuestro contrato.

### Flyweight

ESTE CREO QUE TENÍA OTRO NOMBRE, ES QUE NO LOS TENGO APUNTADOS. El patrón Flyweight (u objeto ligero) sirve para eliminar o reducir la redundancia cuando tenemos gran cantidad de objetos que contienen información idéntica, además de lograr un equilibrio entre flexibilidad y rendimiento (uso de recursos)

- - - -

Estas definiciones las ha sacado de una busqueda rápida en google, es más por tener los patrones recomendados aquí a mano para todos y saber que debemos usarlos. Eran unos 6, no me sale ahora el nombre de los otros.
