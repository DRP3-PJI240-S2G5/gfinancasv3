import { defineStore } from "pinia"
import accountsApi from "@/api/accounts.api.js"

export const useAccountsStore = defineStore("accountsStore", {
  state: () => ({
    loading: false,
    loggedUser: null,
    users: [],
  }),
  actions: {
    async getUsers() {
      this.loading = true
      try {
        this.users = await accountsApi.listUsers()
      } finally {
        this.loading = false
      }
    },
    async whoAmI() {
      const response = await accountsApi.whoami()
      const loggedIn = response.authenticated && response.user
      this.loggedUser = null
      if (loggedIn) {
        this.loggedUser = response.user
        // Adiciona roles do usuário
        this.loggedUser.roles = response.user.roles || []
      }
      return this.loggedUser
    },
    async login(username, password) {
      this.loading = true
      const response = await accountsApi.login(username, password)
      this.loading = false
      if (!response) {
        return
      }
      this.loggedUser = response
      // Adiciona roles após o login
      this.loggedUser.roles = response.roles || []
      return this.loggedUser
    },
    async logout() {
      this.loading = true
      const response = await accountsApi.logout()
      this.loading = false
      if (!response.authenticated) {
        this.loggedUser = null
        return true
      }
      return false
    },
    async addNewUser(newUser) {
      const user = await accountsApi.addNewUser(newUser)
      this.users.push(user)
      return user
    },
  },
})
