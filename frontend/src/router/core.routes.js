// Composables
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"
import GestaoView from "@/views/core/GestaoView.vue"
import GastosView from "@/views/core/GastosView.vue"
import InitialView from "@/views/base/InitialView.vue"
import RelatoriosView from "@/views/core/RelatoriosView.vue"
import ConsultasView from "@/views/core/ConsultasView.vue"
import GestaoDepartamentosView from "@/views/core/GestaoDepartamentosView.vue"

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
      {
        path: "gdepartamentos",
        name: "gdepartamentos",
        component: GestaoDepartamentosView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
      {
        path: "consultas",
        name: "consultas",
        component: ConsultasView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
      {
        path: "relatorios",
        name: "relatorios",
        component: RelatoriosView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
    ],
  },
]
