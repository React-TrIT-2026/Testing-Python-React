import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { createApiClient } from "./api/client.js";
import App from "./App.jsx";
import "./styles/tokens.css";
import "./styles/base.css";
import "./styles/app.css";

const api = createApiClient({
  baseUrl: import.meta.env.VITE_API_URL ?? "/api",
});

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App api={api} />
  </StrictMode>,
);
