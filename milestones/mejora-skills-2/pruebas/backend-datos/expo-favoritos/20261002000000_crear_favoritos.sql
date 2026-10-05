-- Migración: crea la tabla de favoritos con sus reglas de acceso.
-- Va en supabase/migrations/ del proyecto destino (nombre generado por la
-- CLI de Supabase con `supabase migration new crear_favoritos`; confirma el
-- comando en la doc oficial al usarlo).
-- RLS y políticas se crean en la MISMA migración que la tabla: la tabla
-- nunca existe expuesta sin reglas.

create table public.favoritos (
  id         uuid        primary key default gen_random_uuid(),
  user_id    uuid        not null default auth.uid()
                         references auth.users (id) on delete cascade,
  item_id    text        not null,
  titulo     text        not null,
  creado_en  timestamptz not null default now(),
  constraint favoritos_item_id_check check (char_length(btrim(item_id)) between 1 and 100),
  constraint favoritos_titulo_check  check (char_length(btrim(titulo))  between 1 and 200),
  constraint favoritos_user_item_key unique (user_id, item_id)
);

create index favoritos_user_creado_idx on public.favoritos (user_id, creado_en desc);

-- Reglas de acceso por fila (RLS), activas desde el primer día.
alter table public.favoritos enable row level security;

create policy "Cada usuario ve sus favoritos"
  on public.favoritos for select
  to authenticated
  using ( (select auth.uid()) = user_id );

create policy "Cada usuario agrega sus favoritos"
  on public.favoritos for insert
  to authenticated
  with check ( (select auth.uid()) = user_id );

create policy "Cada usuario quita sus favoritos"
  on public.favoritos for delete
  to authenticated
  using ( (select auth.uid()) = user_id );

-- Sin política de update: un favorito no se edita.

-- Permisos por columna: el cliente solo escribe item_id y titulo; id,
-- user_id y creado_en los asigna siempre el servidor.
revoke all on public.favoritos from anon;
revoke insert, update on public.favoritos from authenticated;
grant insert (item_id, titulo) on public.favoritos to authenticated;
