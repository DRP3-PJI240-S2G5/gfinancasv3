import { createRouter, createWebHistory } from "vue-router"
import accountsRoutes from "./accounts.routes"
import { useAccountsStore } from "@/stores/accountsStore" // Importa a store de autenticação
import baseRoutes from "./base.routes"
import coreRoutes from "./core.routes"
import Page404View from "@/views/base/Page404View.vue"


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...baseRoutes,
    ...accountsRoutes,
    ...coreRoutes,
    {
      path: "/:pathMatch(.*)*",
      name: "page-not-found-404",
      component: Page404View,
    },
  ],
})

// Guarda de rota
router.beforeEach(async (to, from, next) => {
  const accountsStore = useAccountsStore()

  // Verifica se a rota requer autenticação
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Verifica se o usuário está logado
    if (!accountsStore.loggedUser) {
      // Chama o whoAmI para verificar o login atual se o usuário não estiver no estado
      await accountsStore.whoAmI()

      if (!accountsStore.loggedUser) {
        // Redireciona para a página de login se não estiver autenticado
        return next({ name: 'accounts-login' })
      }
    }
  }

  // Caso contrário, segue normalmente
  next()
})
export default router
