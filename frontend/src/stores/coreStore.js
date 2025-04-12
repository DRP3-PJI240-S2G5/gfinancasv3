import { defineStore } from "pinia"
import coreApi from "@/api/core.api.js"

export const useCoreStore = defineStore("coreStore", {
  state: () => ({
    departamentos: [],
    elementos: [],
    tipoGastos: [],
    despesas: [],
    departamentosLoading: false,
    elementosLoading: false,
    tipoGastosLoading: false,
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
  },
})
