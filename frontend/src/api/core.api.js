import api from "./config.js"

export default {
  getDepartamentos: async () => {
    const response = await api.get("/api/core/departamentos/list")
    return response.data
  },
  addNewDepartamento: async (description) => {
    const json = { description }
    const response = await api.post(
      "/api/core/departamentos/add",
      json
    )
    return response.data
  },
}
