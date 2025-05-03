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
      console.log('Iniciando carregamento de usuários')
      this.loading = true
      try {
        this.users = await accountsApi.listUsers()
        console.log('Usuários carregados:', this.users)
      } catch (error) {
        console.error('Erro ao carregar usuários:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async whoAmI() {
      console.log('Verificando usuário logado')
      try {
        const response = await accountsApi.whoami()
        console.log('Resposta do whoami:', response)
        const loggedIn = response.authenticated && response.user
        this.loggedUser = null
        if (loggedIn) {
          this.loggedUser = response.user
          this.loggedUser.roles = response.user.roles || []
          console.log('Usuário logado:', this.loggedUser)
        }
        return this.loggedUser
      } catch (error) {
        console.error('Erro ao verificar usuário logado:', error)
        throw error
      }
    },
    async login(username, password) {
      console.log('Iniciando processo de login')
      this.loading = true
      try {
        const response = await accountsApi.login(username, password)
        console.log('Resposta do login:', response)
        this.loading = false
        if (!response) {
          console.log('Login falhou - resposta vazia')
          return
        }
        this.loggedUser = response
        this.loggedUser.roles = response.roles || []
        console.log('Login realizado com sucesso:', this.loggedUser)
        return this.loggedUser
      } catch (error) {
        console.error('Erro no processo de login:', error)
        this.loading = false
        throw error
      }
    },
    async logout() {
      console.log('Iniciando processo de logout')
      this.loading = true
      try {
        const response = await accountsApi.logout()
        console.log('Resposta do logout:', response)
        this.loading = false
        if (!response.authenticated) {
          this.loggedUser = null
          console.log('Logout realizado com sucesso')
          return true
        }
        console.log('Logout falhou - usuário ainda autenticado')
        return false
      } catch (error) {
        console.error('Erro no processo de logout:', error)
        this.loading = false
        throw error
      }
    },
    async addNewUser(newUser) {
      console.log('Adicionando novo usuário:', newUser)
      try {
        const user = await accountsApi.addNewUser(newUser)
        console.log('Novo usuário criado:', user)
        this.users.push(user)
        return user
      } catch (error) {
        console.error('Erro ao adicionar novo usuário:', error)
        throw error
      }
    },
  },
})
