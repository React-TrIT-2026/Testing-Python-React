import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: !process.env.STUDIO_NO_BROWSER,
    watch: {
      ignored: [
        "**/node_modules/**",
        "**/coverage/**",
        "**/dist/**",
        "**/test-results/**",
        "**/playwright-report/**",
        "**/quality-playground/**",
        "**/test/**",
        "**/e2e/**",
        "**/.app/**",
      ],
    },
    proxy: {
      "/api": {
        target: process.env.STUDIO_API_URL ?? "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  preview: {
    port: 4173,
    proxy: {
      "/api": {
        target: process.env.STUDIO_API_URL ?? "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
