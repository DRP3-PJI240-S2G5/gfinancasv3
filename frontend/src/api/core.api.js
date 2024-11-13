import api from "./config.js"

export default {
  getDepartamentos: async () => {
    const response = await api.get("/api/core/departamentos/list")
    return response.data
  },
  addNewDepartamento: async (newDepartamento) => {
    const response = await api.post(
      "/api/core/departamentos/add",
      newDepartamento
    )
    return response.data
  },
  updateDepartamento: async (updatedDepartamento) => {
    const response = await api.put(
      "/api/core/departamentos/update",
      updatedDepartamento
    );
    return response.data;
  },
}
