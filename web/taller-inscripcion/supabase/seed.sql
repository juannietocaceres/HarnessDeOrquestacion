-- Datos semilla SOLO para desarrollo local. Datos ficticios.
-- Un taller de ejemplo (los demás se gestionan en el panel de Supabase).
-- Corre como rol de base de datos (fuera de RLS). No crea inscripciones ni
-- usuarios: el estudiante se registra desde la app (Supabase Auth).

insert into public.talleres (id, titulo, descripcion, inicia_en, cupo)
values (
  '11111111-1111-4111-8111-111111111111',
  'Introducción a Git y GitHub',
  'Taller práctico de ejemplo: control de versiones desde cero.',
  '2026-11-14T15:00:00Z',
  30
)
on conflict (id) do nothing;
