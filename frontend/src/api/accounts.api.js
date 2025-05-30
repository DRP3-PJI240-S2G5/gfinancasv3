import api from "./config.js"

export default {
  whoami: async () => {
    const response = await api.get("/api/accounts/whoami")
    return response.data
  },
  login: async (username, password) => {
    const json = {username, password}
    const response = await api.post(
      "/api/accounts/login",
      json
    )
    return response.data
  },
  logout: async () => {
    const response = await api.post("/api/accounts/logout")
    return response.data
  },
  addNewUser: async (newUser) => {
    const response = await api.post(
      "/api/accounts/add-user",
      newUser
    )
    return response.data
  },
  listUsers: async() => {
    const response = await api.get("/api/accounts/list-users")
    return response.data.users
  },
  listRoles: async() => {
    const response = await api.get("/api/accounts/list-roles")
    return response.data.roles
  },
}
