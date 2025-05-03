import { defineStore } from "pinia"

export const useBaseStore = defineStore("baseStore", {
  state: () => ({
    errorMessage: undefined,
    showErrorMessage: false,
    snackbarMessage: undefined,
    showSnackbarMessage: false,
    type: "success",
  }),
  actions: {
    setShowErrorMessage(errorMessage) {
      console.log('Definindo mensagem de erro:', errorMessage)
      this.errorMessage = errorMessage
      this.showErrorMessage = !!errorMessage
    },
    showSnackbar(message, type) {
      console.log('Mostrando snackbar:', { message, type })
      this.type = type
      this.snackbarMessage = message
      this.showSnackbarMessage = !!message
    },
  },
})
