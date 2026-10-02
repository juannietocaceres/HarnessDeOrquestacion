Quiero armar un panel de administración de tareas para una demo de clase.
Primero hay que definir cómo es una tarea: sus campos con tipos y
validaciones, documentado en schema/tareas.md con un ejemplo en JSON; como
mínimo id, título, estado y fecha de creación, y el estado solo puede ser
pendiente, en_curso o hecha. Con ese modelo, documentar la API REST para
crear y listar tareas (todavía no tengo claro cómo debería ser ese
contrato). Cuando esté el contrato, tres piezas de UI estáticas en
HTML/CSS/JS sin build: una lista de tareas (ui/lista-tareas.html) que
muestre al menos 3 tareas de ejemplo con el estado bien distinguible, un
formulario para crear una tarea con los campos que pida el contrato
(ui/nueva-tarea.html) y un contador de pendientes (ui/badge-pendientes.html)
con un número y una etiqueta clara. Que la UI no parezca una plantilla
genérica. Quiero máximo 2 tareas en paralelo, para que se note el límite de
concurrencia en la demo.
