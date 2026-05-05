/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
  readonly VITE_API_ROLE?: string
  readonly VITE_DEBUG_MODE?: string
  readonly VITE_LEGACY_TILE_URL?: string
  readonly VITE_MAP_GEOMETRY_ENABLED?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
