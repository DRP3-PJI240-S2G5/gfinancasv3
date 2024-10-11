// Composables
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"
import GestaoView from "@/views/core/GestaoView.vue"
import GastosView from "@/views/core/GastosView.vue"
import InitialView from "@/views/base/InitialView.vue"

export default [
  {
    path: "/",
    component: DefaultLayout,
    children: [
      {
        path: "inicial",
        name: "inicial",
        component: InitialView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
      {
        path: "gastos",
        name: "gastos",
        component: GastosView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
      {
        path: "gestao",
        name: "gestao",
        component: GestaoView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
    ],
  },
]
