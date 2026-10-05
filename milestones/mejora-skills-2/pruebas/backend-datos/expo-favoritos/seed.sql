-- Datos semilla SOLO para desarrollo local (va en supabase/seed.sql del
-- proyecto destino). Datos ficticios; nunca datos reales de personas.
--
-- Depende de dos usuarios de prueba creados con Supabase Auth en la base
-- LOCAL (paso manual: crearlos desde el panel local o con el registro de la
-- propia app, con correos ana@example.test y beto@example.test). Si no
-- existen, estos insert no agregan filas. Corre como rol de base de datos
-- (fuera de RLS), por eso puede fijar user_id.

insert into public.favoritos (user_id, item_id, titulo)
select u.id, v.item_id, v.titulo
from auth.users u
join (values
  ('ana@example.test',  'receta-1', 'Arepas de queso'),
  ('ana@example.test',  'receta-2', 'Sancocho'),
  ('beto@example.test', 'receta-1', 'Arepas de queso')
) as v (email, item_id, titulo) on v.email = u.email
on conflict (user_id, item_id) do nothing;
