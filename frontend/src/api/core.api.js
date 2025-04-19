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
  getElementos: async () => {
    const response = await api.get("/api/core/elementos/list")
    return response.data
  },
  getTipoGastos: async () => {
    const response = await api.get("/api/core/tipo-gastos/list")
    return response.data
  },
  getTipoGastosPorElemento: async (elementoId) => {
    const response = await api.get(`/api/core/tipo-gastos/por-elemento/${elementoId}`);
    return response.data;
  },
  // Função para adicionar despesa
  addDespesa: async (novaDespesa) => {
    const response = await api.post(
      "/api/core/despesas/add",
      novaDespesa);
    return response.data;
  },

  // Função para atualizar despesa
  updateDespesa: async (updatedDespesa) => {
    const response = await api.put("/api/core/despesas/update", updatedDespesa);
    return response.data;
  },
  // Função para buscar despesas paginadas de um departamento
  getDespesasPorDepartamento: async (departamentoId, page = 1, perPage = 10) => {
    const response = await api.get(
      `/api/core/despesas/list/${departamentoId}?page=${page}&per_page=${perPage}`
    )
    return {
      despesas: response.data.despesas,                    // lista principal
      totalPaginas: response.data.paginacao.total_paginas  // total de páginas
    }
  },
  // Função para deletar uma despesa
  deleteDespesa: async (despesaId) => {
    const response = await api.delete(`/api/core/despesas/delete/${despesaId}`);
    return response.data;
  },
  getLeisNormas: async () => {
    const response = await api.get("/api/core/leis-normas/list")
    return response.data
  },
}
