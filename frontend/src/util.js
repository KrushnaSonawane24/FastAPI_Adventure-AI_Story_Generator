// API Base URL - uses environment variable or falls back to localhost
export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Production: Set VITE_API_URL in Render environment variables
// Development: Uses localhost automatically
