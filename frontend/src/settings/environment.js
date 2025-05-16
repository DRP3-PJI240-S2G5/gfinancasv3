export const environment = {
  isDev: import.meta.env.VITE_NODE_ENV === "development",
  isMock: import.meta.env.VITE_API_MOCK === "true",
  apiBaseURL: import.meta.env.VITE_API_BASE_URL,
}
