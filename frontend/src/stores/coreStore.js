import { defineStore } from "pinia"
import coreApi from "@/api/core.api.js"

export const useCoreStore = defineStore("coreStore", {
  state: () => ({
    departamentos: [],
    departamentosLoading: false,
  }),
  actions: {
    async getDepartamentos() {
      this.departamentosLoading = true
      const response = await coreApi.getDepartamentos()
      this.departamentos = response.departamentos
      this.departamentosLoading = false
    },
    async addNewDepartamento(departamentoData) {
      try {
        const response = await coreApi.addNewDepartamento(departamentoData);
        const newDepartamento = response.data;
        this.departamentos.push(newDepartamento) // Adiciona o novo departamento à lista
        return newDepartamento
      } catch (error) {
        console.error("Erro ao adicionar departamento:", error)
        return null;
      }
    },
    async updateDepartamento(departamentoId, updatedData) {
      try {
        const updatedDepartamento = await coreApi.updateDepartamento(departamentoId, updatedData)
        // Atualiza o departamento na lista
        const index = this.departamentos.findIndex(dept => dept.id === departamentoId)
        if (index !== -1) {
          this.departamentos[index] = updatedDepartamento
        }
        return updatedDepartamento
      } catch (error) {
        console.error("Erro ao atualizar departamento:", error)
        return null // Garantir que o valor retornado seja algo controlável
      }
    },
  },
})
