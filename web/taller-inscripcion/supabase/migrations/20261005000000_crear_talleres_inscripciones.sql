-- Migración: talleres e inscripciones con RLS en la misma migración.
-- Nombre generado con `supabase migration new crear_talleres_inscripciones`
-- (confirma el comando en la doc oficial al usarlo).
-- Auth: la del proveedor (Supabase Auth). Aquí solo se referencia auth.users.

-- ---------- talleres (los gestiona el organizador en el panel) ----------
create table public.talleres (
  id           uuid        primary key default gen_random_uuid(),
  titulo       text        not null,
  descripcion  text        not null default '',
  inicia_en    timestamptz not null,
  cupo         integer     not null,
  creado_en    timestamptz not null default now(),
  constraint talleres_titulo_check check (char_length(btrim(titulo)) between 1 and 150),
  constraint talleres_descripcion_check check (char_length(descripcion) <= 1000),
  constraint talleres_cupo_check check (cupo between 1 and 1000)
);

-- ---------- inscripciones ----------
create table public.inscripciones (
  id         uuid        primary key default gen_random_uuid(),
  user_id    uuid        not null default auth.uid()
                         references auth.users (id) on delete cascade,
  taller_id  uuid        not null references public.talleres (id) on delete cascade,
  nombre     text        not null,
  creado_en  timestamptz not null default now(),
  constraint inscripciones_nombre_check check (char_length(btrim(nombre)) between 1 and 100),
  constraint inscripciones_user_taller_key unique (user_id, taller_id)
);

create index inscripciones_taller_idx on public.inscripciones (taller_id);

-- ---------- cupo: se valida en la base, no solo en el cliente ----------
-- SECURITY DEFINER porque debe contar TODAS las inscripciones del taller
-- (el estudiante solo ve las suyas bajo RLS). Bloquea la fila del taller
-- para que dos inscripciones simultáneas no sobrepasen el cupo.
create function public.validar_cupo_taller()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_cupo integer;
  v_usadas integer;
begin
  select cupo into v_cupo from public.talleres where id = new.taller_id for update;
  select count(*) into v_usadas from public.inscripciones where taller_id = new.taller_id;
  if v_usadas >= v_cupo then
    raise exception 'taller_lleno' using errcode = 'P0001';
  end if;
  return new;
end;
$$;

revoke all on function public.validar_cupo_taller() from public, anon, authenticated;

create trigger inscripciones_validar_cupo
  before insert on public.inscripciones
  for each row execute function public.validar_cupo_taller();

-- Cupos libres de un taller (para mostrarlos en la UI sin exponer filas ajenas).
create function public.cupos_disponibles(p_taller_id uuid)
returns integer
language sql
stable
security definer
set search_path = ''
as $$
  select t.cupo - (select count(*)::integer from public.inscripciones i where i.taller_id = t.id)
  from public.talleres t
  where t.id = p_taller_id;
$$;

revoke all on function public.cupos_disponibles(uuid) from public, anon;
grant execute on function public.cupos_disponibles(uuid) to authenticated;

-- ---------- RLS: activo desde el primer día ----------
alter table public.talleres enable row level security;
alter table public.inscripciones enable row level security;

-- Talleres: solo lectura para usuarios autenticados. Sin insert/update/delete
-- desde el cliente (el organizador usa el panel, que salta RLS).
create policy "Autenticados ven los talleres"
  on public.talleres for select
  to authenticated
  using ( true );

create policy "Cada estudiante ve sus inscripciones"
  on public.inscripciones for select
  to authenticated
  using ( (select auth.uid()) = user_id );

create policy "Cada estudiante crea sus inscripciones"
  on public.inscripciones for insert
  to authenticated
  with check ( (select auth.uid()) = user_id );

create policy "Cada estudiante cancela sus inscripciones"
  on public.inscripciones for delete
  to authenticated
  using ( (select auth.uid()) = user_id );

-- Sin política de update: una inscripción no se edita (se cancela y se crea otra).

-- Permisos por columna: el cliente solo escribe taller_id y nombre; id,
-- user_id y creado_en los asigna siempre el servidor.
revoke all on public.talleres, public.inscripciones from anon;
revoke insert, update, delete on public.talleres from authenticated;
revoke insert, update on public.inscripciones from authenticated;
grant select on public.talleres to authenticated;
grant insert (taller_id, nombre) on public.inscripciones to authenticated;
