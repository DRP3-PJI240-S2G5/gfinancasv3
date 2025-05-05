import { defineStore } from "pinia"
import coreApi from "@/api/core.api.js"
import { useBaseStore } from './baseStore'

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
    verbasPaginacao: null,
    totalDespesas: {},
    responsabilidades: []
  }),
  actions: {
    async getDepartamentos() {
      this.departamentosLoading = true
      const response = await coreApi.getDepartamentos()
      this.departamentos = response.departamentos
      this.departamentosLoading = false
    },
    async addNewDepartamento(departamento) {
      const newDepartamento = await coreApi.addNewDepartamento(departamento)
      return newDepartamento
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
      this.elementosLoading = true
      const response = await coreApi.getElementos()
      this.elementos = response.elementos
      this.elementosLoading = false
    },
    async getTipoGastos() {
      this.tipoGastosLoading = true
      const response = await coreApi.getTipoGastos()
      this.tipoGastos = response.tipoGastos
      this.tipoGastosLoading = false
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
    async deleteTipoGasto(tipoGastoId) {
      try {
        await coreApi.deleteTipoGasto(tipoGastoId)
        this.tipoGastos = this.tipoGastos.filter(tg => tg.id !== tipoGastoId)
      } catch (e) {
        console.error("Erro ao deletar tipo de gasto:", e)
        throw e
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
        // Atualiza o estado com o novo total
        this.totalDespesas[departamentoId] = response;
        return response;
      } catch (e) {
        console.error("Erro ao buscar total de despesas do departamento:", e);
        throw e;
      }
    },
    async getTotalDespesasDepartamentoAPartirData(departamentoId, data_inicio) {
      this.loading = true;
      try {
        const response = await coreApi.getTotalDespesasDepartamentoAPartirData(departamentoId, data_inicio);
        return response;
      } catch (error) {
        this.error = error;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    // Busca despesas de um departamento em um período específico
    async getDespesasPorDepartamentoPeriodo(departamentoId, data_inicio, data_termino, page = 1, perPage = 10) {
      this.despesasLoading = true;
      try {
        const response = await coreApi.getDespesasPorDepartamentoPeriodo(
          departamentoId,
          data_inicio,
          data_termino,
          page,
          perPage
        );
        this.despesas = response.despesas;
        this.totalPaginas = response.totalPaginas;
        return response;
      } catch (error) {
        this.error = error;
        throw error;
      } finally {
        this.despesasLoading = false;
      }
    },
    // Busca o total de despesas de um departamento em um período específico
    async getTotalDespesasDepartamentoPeriodo(departamentoId, data_inicio, data_termino) {
      this.loading = true;
      try {
        const response = await coreApi.getTotalDespesasDepartamentoPeriodo(
          departamentoId,
          data_inicio,
          data_termino
        );
        return response;
      } catch (error) {
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
      this.verbasLoading = true
      try {
        const data = await coreApi.addVerba(verba)
        this.verbas.push(data)
        this.error = null
        return data
      } catch (err) {
        this.error = err.message
        console.error('Erro ao adicionar verba:', err)
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
      this.verbasLoading = true
      try {
        const response = await coreApi.getVerba(id)
        this.error = null
        return response
      } catch (err) {
        this.error = err.message
        console.error('Erro ao buscar verba:', err)
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
    },
    // Elementos
    async addElemento(elemento) {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        // Validações
        if (!elemento.elemento || !elemento.descricao) {
          throw new Error('Elemento e descrição são obrigatórios')
        }
        if (elemento.elemento.length > 256 || elemento.descricao.length > 256) {
          throw new Error('Elemento e descrição não podem ter mais de 256 caracteres')
        }

        const novoElemento = await coreApi.addNewElemento(elemento)
        this.elementos.push(novoElemento)
        baseStore.showSnackbar('Elemento adicionado com sucesso!')
        return novoElemento
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateElemento(elemento) {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        // Validações
        if (!elemento.id) {
          throw new Error('ID do elemento é obrigatório')
        }
        if (!elemento.elemento || !elemento.descricao) {
          throw new Error('Elemento e descrição são obrigatórios')
        }
        if (elemento.elemento.length > 256 || elemento.descricao.length > 256) {
          throw new Error('Elemento e descrição não podem ter mais de 256 caracteres')
        }

        const elementoAtualizado = await coreApi.updateElemento(elemento)
        const index = this.elementos.findIndex(e => e.id === elemento.id)
        if (index !== -1) {
          this.elementos[index] = elementoAtualizado
        }
        baseStore.showSnackbar('Elemento atualizado com sucesso!')
        return elementoAtualizado
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteElemento(id) {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        // Validações
        if (!id) {
          throw new Error('ID do elemento é obrigatório')
        }

        await coreApi.deleteElemento(id)
        this.elementos = this.elementos.filter(e => e.id !== id)
        baseStore.showSnackbar('Elemento removido com sucesso!')
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    // Tipo de Gastos
    async addTipoGasto(tipoGasto) {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        // Validações
        if (!tipoGasto.tipoGasto || !tipoGasto.descricao) {
          throw new Error('Tipo de gasto e descrição são obrigatórios')
        }
        if (tipoGasto.tipoGasto.length > 256 || tipoGasto.descricao.length > 256) {
          throw new Error('Tipo de gasto e descrição não podem ter mais de 256 caracteres')
        }

        const novoTipoGasto = await coreApi.addNewTipoGasto(tipoGasto)
        this.tipoGastos.push(novoTipoGasto)
        baseStore.showSnackbar('Tipo de gasto adicionado com sucesso!')
        return novoTipoGasto
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateTipoGasto(tipoGasto) {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        // Validações
        if (!tipoGasto.id) {
          throw new Error('ID do tipo de gasto é obrigatório')
        }
        if (!tipoGasto.tipoGasto || !tipoGasto.descricao) {
          throw new Error('Tipo de gasto e descrição são obrigatórios')
        }
        if (tipoGasto.tipoGasto.length > 256 || tipoGasto.descricao.length > 256) {
          throw new Error('Tipo de gasto e descrição não podem ter mais de 256 caracteres')
        }

        const tipoGastoAtualizado = await coreApi.updateTipoGasto(tipoGasto)
        const index = this.tipoGastos.findIndex(tg => tg.id === tipoGasto.id)
        if (index !== -1) {
          this.tipoGastos[index] = tipoGastoAtualizado
        }
        baseStore.showSnackbar('Tipo de gasto atualizado com sucesso!')
        return tipoGastoAtualizado
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    // Elemento-TipoGasto
    async addElementoTipoGasto(elementoId, tipoGastoId) {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        // Validações
        if (!elementoId || !tipoGastoId) {
          throw new Error('ID do elemento e ID do tipo de gasto são obrigatórios')
        }

        const relacionamento = await coreApi.addElementoTipoGasto(elementoId, tipoGastoId)
        baseStore.showSnackbar('Relacionamento adicionado com sucesso!')
        return relacionamento
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteElementoTipoGasto(id) {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        // Validações
        if (!id) {
          throw new Error('ID do relacionamento é obrigatório')
        }

        await coreApi.deleteElementoTipoGasto(id)
        baseStore.showSnackbar('Relacionamento removido com sucesso!')
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    // Responsabilidades
    async addResponsabilidade(responsabilidade) {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        // Validações
        if (!responsabilidade.usuario_id || !responsabilidade.departamento_id) {
          throw new Error('ID do usuário e ID do departamento são obrigatórios')
        }

        const novaResponsabilidade = await coreApi.addResponsabilidade(responsabilidade)
        this.responsabilidades.push(novaResponsabilidade)
        baseStore.showSnackbar('Responsabilidade adicionada com sucesso!')
        return novaResponsabilidade
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    async getResponsabilidades() {
      const baseStore = useBaseStore()
      this.loading = true
      this.error = null

      try {
        const responsabilidades = await coreApi.getResponsabilidades()
        this.responsabilidades = responsabilidades
        return responsabilidades
      } catch (error) {
        this.error = error.message
        baseStore.showSnackbar(error.message, 'error')
        throw error
      } finally {
        this.loading = false
      }
    }
  },
})
