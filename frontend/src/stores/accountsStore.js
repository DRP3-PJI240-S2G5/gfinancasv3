import { defineStore } from "pinia"
import AccountsApi from "@/api/accounts.api.js"
import users from "@/apimock/fixtures/users"

export const useAccountsStore = defineStore("accountsStore", {
  state: () => ({
    loading: false,
    loggedUser: null,
    users: [],
  }),
  actions: {
    async whoAmI() {
      this.loading = true;
      const response = await AccountsApi.whoami()
      this.loading = false;
      const loggedIn = response.authenticated && response.user
      this.loggedUser = null
      if (loggedIn) {
        this.loggedUser = response.user
      }
      return this.loggedUser
    },
    async login(username, password) {
      this.loading = true
      const response = await AccountsApi.login(username, password)
      this.loading = false
      if (!response) {
        return
      }
      this.loggedUser = response
      return this.loggedUser
    },
    async logout() {
      this.loading = true
      const response = await AccountsApi.logout()
      this.loading = false
      if (!response.authenticated) {
        this.loggedUser = null
        return true
      }
      return false
    },
    async get_users() {
      this.loading = true;
      try {
        const response = await AccountsApi.get_users(); // Chamando a API de usuários
        this.users = response.users; // Armazenando os usuários no estado da store
      } catch (error) {
        console.error("Erro ao obter usuários:", error);
      } finally {
        this.loading = false;
      }
    },
  },
})
