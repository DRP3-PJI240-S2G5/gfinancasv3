import { createServer, Model } from "miragejs"

import users from "./fixtures/users"
import { serializers } from "./serializers"
import { routes } from "./routes"
import { factories } from "./factories"

const mockConfig = {
  models: {
    user: Model,
    departamento: Model,
  },
  seeds(server) {
    server.loadFixtures()
    server.createList("departamento", 2)
  },
  serializers,
  factories,
  routes,
}

export const mockServer = function () {
  let mockServer = createServer(mockConfig)
  mockServer.db.loadData({
    users,
  })
  return mockServer
}
