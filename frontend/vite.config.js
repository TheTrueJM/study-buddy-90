import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [
    svelte({
      onwarn: (warning, handler) => {
        if (warning.code && String(warning.code).toLowerCase().startsWith('a11y_')) return;
        handler(warning);
      },
    }),
  ],
})
