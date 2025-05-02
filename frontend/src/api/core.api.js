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
  getDespesasPorDepartamentoAPartirData: async (departamentoId, data_inicio, page = 1, perPage = 10) => {
    const response = await api.get(
      `/api/core/despesas/list/departamento/${departamentoId}/apartir-data/${data_inicio}?page=${page}&per_page=${perPage}`
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
  // Função para buscar o total de despesas de um departamento
  getTotalDespesasDepartamento: async (departamentoId) => {
    const response = await api.get(`/api/core/departamentos/total-despesas/${departamentoId}`);
    return response.data;
  },
  getTotalDespesasDepartamentoAPartirData: async (departamentoId, data_inicio) => {
    const response = await api.get(`/api/core/departamentos/total-despesas-apartir-data/${departamentoId}/data/${data_inicio}`);
    return response.data;
  },
  // Funções para gerenciar subordinações
  getSubordinacoes: async () => {
    const response = await api.get("/api/core/subordinacoes/list")
    return response.data
  },
  createSubordinacao: async (subordinacao) => {
    const response = await api.post("/api/core/subordinacoes/add", subordinacao)
    return response.data
  },
  updateSubordinacao: async (subordinacao) => {
    const response = await api.put(`/api/core/subordinacoes/update/${subordinacao.id}`, subordinacao)
    return response.data
  },
  deleteSubordinacao: async (id) => {
    if (!id) {
      throw new Error('ID da subordinação é obrigatório')
    }
    const response = await api.delete(`/api/core/subordinacoes/delete/${id}`)
    return response.data
  },
  // Funções para gerenciar verbas
  getVerbas: async (page = 1, perPage = 10) => {
    const response = await api.get(`/api/core/verbas/list?page=${page}&per_page=${perPage}`)
    return {
      verbas: response.data.verbas,
      paginacao: response.data.paginacao
    }
  },
  addVerba: async (verba) => {
    if (!verba.valor || !verba.departamento_id || !verba.ano) {
      throw new Error('Valor, departamento e ano são obrigatórios')
    }
    const response = await api.post("/api/core/verbas/add", verba)
    return response.data
  },
  updateVerba: async (verba) => {
    if (!verba.id) {
      throw new Error('ID da verba é obrigatório')
    }
    if (!verba.valor || !verba.departamento_id || !verba.ano) {
      throw new Error('Valor, departamento e ano são obrigatórios')
    }
    const response = await api.put(`/api/core/verbas/update/${verba.id}`, verba)
    return response.data
  },
  deleteVerba: async (id) => {
    if (!id) {
      throw new Error('ID da verba é obrigatório')
    }
    const response = await api.delete(`/api/core/verbas/delete/${id}`)
    return response.data
  },
  getVerba: async (id) => {
    if (!id) {
      throw new Error('ID da verba é obrigatório')
    }
    const response = await api.get(`/api/core/verbas/get/${id}`)
    return response.data
  },
  getVerbasDepartamento: async (departamentoId) => {
    if (!departamentoId) {
      throw new Error('ID do departamento é obrigatório')
    }
    const response = await api.get(`/api/core/verbas/departamento/${departamentoId}`)
    return response.data
  },
  getUltimaVerbaDepartamento: async (departamentoId) => {
    if (!departamentoId) {
      throw new Error('ID do departamento é obrigatório')
    }
    const response = await api.get(`/api/core/verbas/ultima-do-departamento/${departamentoId}`)
    return response.data
  },
  
  getVerbaDepartamentoAno: async (departamentoId, ano) => {
    if (!departamentoId || !ano) {
      throw new Error('ID do departamento e ano são obrigatórios')
    }
    const response = await api.get(`/api/core/verbas/departamento/${departamentoId}/ano/${ano}`)
    return response.data
  }
}
