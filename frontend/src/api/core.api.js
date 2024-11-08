  import api from "./config.js"

  export default {
    getDepartamentos: async () => {
      const response = await api.get("/api/core/departamentos/list")
      return response.data
    },
    addNewDepartamento: async (departamentoData) => {
      const response = await api.post(
        "/api/core/departamentos/add", 
        departamentoData); 
      return response.data;
    },
    updateDepartamento: async (departamentoId, updates) => {
      const response = await api.put(`/api/core/departamentos/update/${departamentoId}`, updates)
      return response.data
    },
  
    // Despesas
    getDespesas: async () => {
      const response = await api.get("/api/core/despesas/list")
      return response.data
    },
    addNewDespesa: async (despesaData) => {
      const response = await api.post("/api/core/despesas/add", despesaData)
      return response.data
    },
    updateDespesa: async (despesaId, updates) => {
      const response = await api.put(`/api/core/despesas/update/${despesaId}`, updates)
      return response.data
    },
  
    // Verbas
    getVerbas: async () => {
      const response = await api.get("/api/core/verbas/list")
      return response.data
    },
    addNewVerba: async (verbaData) => {
      const response = await api.post("/api/core/verbas/add", verbaData)
      return response.data
    },
    updateVerba: async (verbaId, updates) => {
      const response = await api.put(`/api/core/verbas/update/${verbaId}`, updates)
      return response.data
    },
  
    // Elementos
    getElementos: async () => {
      const response = await api.get("/api/core/elementos/list")
      return response.data
    },
    addNewElemento: async (nome) => {
      const json = { nome }
      const response = await api.post("/api/core/elementos/add", json)
      return response.data
    },
    updateElemento: async (elementoId, updates) => {
      const response = await api.put(`/api/core/elementos/update/${elementoId}`, updates)
      return response.data
    },
  
    // Tipos de Gasto
    getTiposGasto: async () => {
      const response = await api.get("/api/core/tiposgastos/list")
      return response.data
    },
    addNewTipoGasto: async (descricao) => {
      const json = { descricao }
      const response = await api.post("/api/core/tiposgastos/add", json)
      return response.data
    },
    updateTipoGasto: async (tipoGastoId, updates) => {
      const response = await api.put(`/api/core/tiposgastos/update/${tipoGastoId}`, updates)
      return response.data
    },
  }
