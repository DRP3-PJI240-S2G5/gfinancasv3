import { defineStore } from "pinia"
import coreApi from "@/api/core.api.js"

export const useCoreStore = defineStore("coreStore", {
  state: () => ({
    departamentos: [],
    elementos: [],
    tipoGastos: [],
    despesas: [],
    subordinacoes: [],
    departamentosLoading: false,
    elementosLoading: false,
    tipoGastosLoading: false,
    despesasLoading: false,
    subordinacoesLoading: false,
    totalPaginas: 0,
    verbas: [],
    verbasLoading: false,
    loading: false,
    error: null,
    verbasPaginacao: null
  }),
  actions: {
    async getDepartamentos() {
      console.log('Iniciando carregamento de departamentos')
      this.departamentosLoading = true
      try {
        const response = await coreApi.getDepartamentos()
        console.log('Departamentos carregados:', response.departamentos)
        this.departamentos = response.departamentos
      } catch (error) {
        console.error('Erro ao carregar departamentos:', error)
        throw error
      } finally {
        this.departamentosLoading = false
      }
    },
    async addNewDepartamento(departamento) {
      console.log('Adicionando novo departamento:', departamento)
      try {
        const newDepartamento = await coreApi.addNewDepartamento(departamento)
        console.log('Novo departamento criado:', newDepartamento)
        return newDepartamento
      } catch (error) {
        console.error('Erro ao adicionar departamento:', error)
        throw error
      }
    },
    async updateDepartamento(updatedDepartamento) {
      const departamento = await coreApi.updateDepartamento(updatedDepartamento);
      // Atualiza o departamento na lista
      const index = this.departamentos.findIndex(d => d.id === departamento.id);
      if (index !== -1) {
        this.departamentos[index] = departamento;
      }
      return departamento;
    },
    async getElementos() {
      console.log('Iniciando carregamento de elementos')
      this.elementosLoading = true
      try {
        const response = await coreApi.getElementos()
        console.log('Elementos carregados:', response.elementos)
        this.elementos = response.elementos
      } catch (error) {
        console.error('Erro ao carregar elementos:', error)
        throw error
      } finally {
        this.elementosLoading = false
      }
    },
    async getTipoGastos() {
      console.log('Iniciando carregamento de tipos de gasto')
      this.tipoGastosLoading = true
      try {
        const response = await coreApi.getTipoGastos()
        console.log('Tipos de gasto carregados:', response.tipoGastos)
        this.tipoGastos = response.tipoGastos
      } catch (error) {
        console.error('Erro ao carregar tipos de gasto:', error)
        throw error
      } finally {
        this.tipoGastosLoading = false
      }
    },
    async getTipoGastosPorElemento(elementoId) {
      try {
        const response = await coreApi.getTipoGastosPorElemento(elementoId)
        return response.tipo_gastos
      } catch (e) {
        console.error("Erro ao buscar tipos de gasto por elemento:", e)
        return []
      }
    },
    // Função para adicionar uma nova despesa
    async addDespesa(novaDespesa) {
      try {
        const despesa = await coreApi.addDespesa(novaDespesa)
        this.despesas.push(despesa) // Adiciona a despesa à lista de despesas
        return despesa
      } catch (e) {
        console.error("Erro ao adicionar despesa:", e)
        throw e
      }
    },

    // Função para atualizar uma despesa existente
    async updateDespesa(updatedDespesa) {
      try {
        const despesa = await coreApi.updateDespesa(updatedDespesa)
        const index = this.despesas.findIndex(d => d.id === despesa.id)
        if (index !== -1) {
          this.despesas[index] = despesa // Atualiza a despesa na lista
        }
        return despesa
      } catch (e) {
        console.error("Erro ao atualizar despesa:", e)
        throw e
      }
    },
    // Função para carregar despesas de um departamento
    async getDespesasPorDepartamento(departamentoId, page = 1, perPage = 10) {
      this.despesasLoading = true
      try {
        const response = await coreApi.getDespesasPorDepartamento(departamentoId, page, perPage)
        this.despesas = response.despesas  // Armazena as despesas no estado
        this.despesasLoading = false
        return response
      } catch (e) {
        console.error("Erro ao carregar despesas por departamento:", e)
        this.despesasLoading = false
        throw e
      }
    },
    async getDespesasPorDepartamentoAPartirData(departamentoId, data_inicio, page = 1, perPage = 10) {
      this.despesasLoading = true
      try {
        const response = await coreApi.getDespesasPorDepartamentoAPartirData(departamentoId, data_inicio, page, perPage)
        this.despesas = response.despesas  // Armazena as despesas no estado
        this.despesasLoading = false
        return response
      } catch (e) {
        console.error("Erro ao carregar despesas por departamento:", e)
        this.despesasLoading = false
        throw e
      }
    },
    // Função para deletar uma despesa
    async deleteDespesa(despesaId) {
      try {
        await coreApi.deleteDespesa(despesaId);
        // Remove a despesa da lista
        this.despesas = this.despesas.filter(d => d.id !== despesaId);
      } catch (e) {
        console.error("Erro ao deletar despesa:", e);
        throw e;
      }
    },
    // Função para buscar o total de despesas de um departamento
    async getTotalDespesasDepartamento(departamentoId) {
      try {
        const response = await coreApi.getTotalDespesasDepartamento(departamentoId);
        return response;
      } catch (e) {
        console.error("Erro ao buscar total de despesas do departamento:", e);
        throw e;
      }
    },
    async getTotalDespesasDepartamentoAPartirData(departamentoId, data_inicio) {
      console.log('Buscando total de despesas do departamento:', departamentoId, 'a partir de:', data_inicio)
      this.loading = true;
      try {
        const response = await coreApi.getTotalDespesasDepartamentoAPartirData(departamentoId, data_inicio);
        console.log('Total de despesas encontrado:', response)
        return response;
      } catch (error) {
        console.error('Erro ao buscar total de despesas:', error)
        this.error = error;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    // Busca despesas de um departamento em um período específico
    async getDespesasPorDepartamentoPeriodo(departamentoId, data_inicio, data_termino, page = 1, perPage = 10) {
      console.log('Buscando despesas do departamento:', departamentoId, 'período:', data_inicio, 'a', data_termino)
      this.despesasLoading = true;
      try {
        const response = await coreApi.getDespesasPorDepartamentoPeriodo(
          departamentoId,
          data_inicio,
          data_termino,
          page,
          perPage
        );
        console.log('Despesas encontradas:', response.despesas)
        this.despesas = response.despesas;
        this.totalPaginas = response.totalPaginas;
        return response;
      } catch (error) {
        console.error('Erro ao buscar despesas:', error)
        this.error = error;
        throw error;
      } finally {
        this.despesasLoading = false;
      }
    },
    // Busca o total de despesas de um departamento em um período específico
    async getTotalDespesasDepartamentoPeriodo(departamentoId, data_inicio, data_termino) {
      console.log('Buscando total de despesas do departamento:', departamentoId, 'período:', data_inicio, 'a', data_termino)
      this.loading = true;
      try {
        const response = await coreApi.getTotalDespesasDepartamentoPeriodo(
          departamentoId,
          data_inicio,
          data_termino
        );
        console.log('Total de despesas encontrado:', response)
        return response;
      } catch (error) {
        console.error('Erro ao buscar total de despesas:', error)
        this.error = error;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    // Ações para gerenciar subordinações
    async getSubordinacoes() {
      this.subordinacoesLoading = true
      try {
        const response = await coreApi.getSubordinacoes()
        this.subordinacoes = response.subordinacoes
        this.subordinacoesLoading = false
        return response
      } catch (e) {
        console.error("Erro ao carregar subordinações:", e)
        this.subordinacoesLoading = false
        throw e
      }
    },

    async createSubordinacao(novaSubordinacao) {
      try {
        const subordinacao = await coreApi.createSubordinacao(novaSubordinacao)
        this.subordinacoes.push(subordinacao)
        return subordinacao
      } catch (e) {
        console.error("Erro ao adicionar subordinação:", e)
        throw e
      }
    },

    async updateSubordinacao(subordinacaoAtualizada) {
      try {
        const subordinacao = await coreApi.updateSubordinacao(subordinacaoAtualizada)
        const index = this.subordinacoes.findIndex(s => s.id === subordinacao.id)
        if (index !== -1) {
          this.subordinacoes[index] = subordinacao
        }
        return subordinacao
      } catch (e) {
        console.error("Erro ao atualizar subordinação:", e)
        throw e
      }
    },

    async deleteSubordinacao(id) {
      try {
        await coreApi.deleteSubordinacao(id)
        this.subordinacoes = this.subordinacoes.filter(s => s.id !== id)
      } catch (e) {
        console.error("Erro ao deletar subordinação:", e)
        throw e
      }
    },

    // Ações para gerenciar verbas
    async getVerbas(page = 1, perPage = 10) {
      this.verbasLoading = true
      try {
        const response = await coreApi.getVerbas(page, perPage)
        this.verbas = response.verbas
        this.verbasPaginacao = response.paginacao
        this.error = null
        return response
      } catch (err) {
        this.error = err.message
        console.error('Erro ao buscar verbas:', err)
        throw err
      } finally {
        this.verbasLoading = false
      }
    },

    async addVerba(verba) {
      console.log('Adicionando nova verba:', verba)
      this.verbasLoading = true
      try {
        const data = await coreApi.addVerba(verba)
        console.log('Nova verba criada:', data)
        this.verbas.push(data)
        this.error = null
        return data
      } catch (err) {
        console.error('Erro ao adicionar verba:', err)
        this.error = err.message
        throw err
      } finally {
        this.verbasLoading = false
      }
    },

    async updateVerba(verba) {
      this.verbasLoading = true
      try {
        const updatedVerba = await coreApi.updateVerba(verba)
        const index = this.verbas.findIndex(v => v.id === verba.id)
        if (index !== -1) {
          this.verbas[index] = updatedVerba
        }
        this.error = null
        return updatedVerba
      } catch (err) {
        this.error = err.message
        console.error('Erro ao atualizar verba:', err)
        throw err
      } finally {
        this.verbasLoading = false
      }
    },

    async deleteVerba(id) {
      this.verbasLoading = true
      try {
        await coreApi.deleteVerba(id)
        this.verbas = this.verbas.filter(v => v.id !== id)
        this.error = null
      } catch (err) {
        this.error = err.message
        console.error('Erro ao deletar verba:', err)
        throw err
      } finally {
        this.verbasLoading = false
      }
    },

    async getVerba(id) {
      console.log('Buscando verba:', id)
      this.verbasLoading = true
      try {
        const response = await coreApi.getVerba(id)
        console.log('Verba encontrada:', response)
        this.error = null
        return response
      } catch (err) {
        console.error('Erro ao buscar verba:', err)
        this.error = err.message
        throw err
      } finally {
        this.verbasLoading = false
      }
    },

    async getVerbasDepartamento(departamentoId) {
      this.verbasLoading = true
      try {
        const response = await coreApi.getVerbasDepartamento(departamentoId)
        this.verbas = response.verbas
        this.error = null
        return response
      } catch (err) {
        this.error = err.message
        console.error('Erro ao buscar verbas do departamento:', err)
        throw err
      } finally {
        this.verbasLoading = false
      }
    },

    async getVerbaDepartamentoAno(departamentoId, ano) {
      this.verbasLoading = true
      try {
        const response = await coreApi.getVerbaDepartamentoAno(departamentoId, ano)
        this.error = null
        return response
      } catch (err) {
        this.error = err.message
        console.error('Erro ao buscar verba do departamento por ano:', err)
        throw err
      } finally {
        this.verbasLoading = false
      }
    },
    async getUltimaVerbaDepartamento(departamentoId) {
      this.verbasLoading = true
      try {
        const response = await coreApi.getUltimaVerbaDepartamento(departamentoId)
        this.error = null
        return response
      } catch (err) {
        this.error = err.message
        console.error('Erro ao buscar ultima verba do departamento:', err)
        throw err
      } finally {
        this.verbasLoading = false
      }
    }
  },
})
