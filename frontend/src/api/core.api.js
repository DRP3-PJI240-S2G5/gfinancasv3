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
  deleteDepartamento: async (departamentoId) => {
    const response = await api.delete(`/api/core/departamentos/delete/${departamentoId}`);
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
  deleteTipoGasto: async (tipoGastoId) => {
    const response = await api.delete(`/api/core/tipo-gastos/delete/${tipoGastoId}`);
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
    );
    return response.data;
  },
  // Função para buscar despesas de um departamento em um período específico
  getDespesasPorDepartamentoPeriodo: async (departamentoId, data_inicio, data_termino, page = 1, perPage = 10) => {
    const response = await api.get(
      `/api/core/despesas/list/departamento/${departamentoId}/periodo/${data_inicio}/${data_termino}?page=${page}&per_page=${perPage}`
    );
    return {
      despesas: response.data.despesas,
      totalPaginas: response.data.paginacao.total_paginas
    };
  },
  // Função para buscar o total de despesas de um departamento em um período específico
  getTotalDespesasDepartamentoPeriodo: async (departamentoId, data_inicio, data_termino) => {
    const response = await api.get(
      `/api/core/departamentos/total-despesas-periodo/${departamentoId}/data/${data_inicio}/${data_termino}`
    );
    return response.data;
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
  getTotalDespesasPorElemento: async (departamentoId, elementoId) => {
    const response = await api.get(`/api/core/departamentos/total-despesas/${departamentoId}/elemento/${elementoId}`);
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
  },
  // Elementos
  addNewElemento: async (elemento) => {
    try {
      const response = await api.post("/api/core/elementos/add", elemento);
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao adicionar elemento');
    }
  },
  updateElemento: async (elemento) => {
    try {
      const response = await api.put("/api/core/elementos/update", elemento);
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao atualizar elemento');
    }
  },
  deleteElemento: async (id) => {
    try {
      const response = await api.delete(`/api/core/elementos/delete/${id}`);
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao deletar elemento');
    }
  },
  // Tipo de Gastos
  addNewTipoGasto: async (tipoGasto) => {
    try {
      const response = await api.post("/api/core/tipo-gastos/add", tipoGasto);
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao adicionar tipo de gasto');
    }
  },
  updateTipoGasto: async (tipoGasto) => {
    try {
      const response = await api.put("/api/core/tipo-gastos/update", tipoGasto);
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao atualizar tipo de gasto');
    }
  },
  // Elemento-TipoGasto
  addElementoTipoGasto: async (elementoId, tipoGastoId) => {
    try {
      const response = await api.post("/api/core/elemento-tipo-gasto/add", {
        elemento_id: elementoId,
        tipo_gasto_id: tipoGastoId
      });
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao adicionar relacionamento elemento-tipo de gasto');
    }
  },
  deleteElementoTipoGasto: async (id) => {
    try {
      const response = await api.delete(`/api/core/elemento-tipo-gasto/delete/${id}`);
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao deletar relacionamento elemento-tipo de gasto');
    }
  },
  // Responsabilidades
  addResponsabilidade: async (responsabilidade) => {
    try {
      const response = await api.post("/api/core/responsabilidades/add", responsabilidade);
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao adicionar responsabilidade');
    }
  },
  getResponsabilidades: async () => {
    try {
      const response = await api.get("/api/core/responsabilidades/list");
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Erro ao listar responsabilidades');
    }
  },
}
