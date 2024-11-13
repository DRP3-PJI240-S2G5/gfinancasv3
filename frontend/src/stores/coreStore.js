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
  },
})
