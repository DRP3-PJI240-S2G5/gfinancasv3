// Plugins
import vue from "@vitejs/plugin-vue"
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify"

// Utilities
import { defineConfig } from "vite"
import { fileURLToPath, URL } from "node:url"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls },
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
    }),
  ],
  define: { "process.env": {} },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
    extensions: [".js", ".json", ".jsx", ".mjs", ".ts", ".tsx", ".vue"],
  },
  server: {
    host: 'frontend',
    port: 3000,
    hmr: {
      protocol: 'ws', // Usando ws para o protocolo WebSocket
      host: 'localhost', // Host da máquina onde o Vite está sendo executado
      port: 3000, // Porta que o Vite está ouvindo
    },
    cors: true,
    watch: {
      usePolling: true, // Garante que mudanças no sistema de arquivos sejam detectadas
    },
  },
})
