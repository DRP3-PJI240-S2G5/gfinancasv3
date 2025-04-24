// Composables
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"
import GestaoView from "@/views/core/GestaoView.vue"
import GastosView from "@/views/core/GastosView.vue"
import InitialView from "@/views/base/InitialView.vue"
import GDepartamentosView from "@/views/core/GDepartamentosView.vue"
import CategoriasView from "@/views/core/CategoriasView.vue"
import DepartamentosView from "@/views/core/DepartamentosView.vue"
import UsersView from "@/views/accounts/UsersView.vue"

export default [
  {
    path: "/",
    name: "index",
    component: DefaultLayout,
    children: [
      {
        path: "inicial",
        name: "inicial",
        component: InitialView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
      {
        path: "gestao",
        meta: { requiresAuth: true },  // Esta rota requer autenticação
        children: [
          {
            path: "",
            name: "gestao",
            component: GestaoView,
            meta: { requiresAuth: true },  // Esta rota requer autenticação
          },
          {
            path: "gestao-departamentos",
            name: "gestao-departamentos",
            component: GDepartamentosView,
            meta: { requiresAuth: true },  // Esta rota requer autenticação
          },
          {
            path: "usuarios",
            name: "usuarios",
            component: UsersView,
            meta: { requiresAuth: true },
          },
          {
            path: "categorias",
            name: "categorias",
            component: CategoriasView,
            meta: { requiresAuth: true },
          },
          {
            path: 'subordinacoes',
            name: 'SubordinacoesView',
            component: () => import('@/views/core/SubordinacoesView.vue'),
            meta: {
              requiresAuth: true,
              title: 'Subordinações'
            }
          },
          {
            path: 'verbas',
            name: 'verbas',
            component: () => import('@/views/core/VerbasView.vue'),
            meta: {
              requiresAuth: true,
              title: 'Verbas'
            }
          }
        ],
      },
      {
        path: "departamentos",
        name: "departamentos",
        component: DepartamentosView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
      {
        path: "gastos",
        name: "gastos",
        component: GastosView,
        meta: { requiresAuth: true },  // Esta rota requer autenticação
      },
      {
        path: "gastos/:departamento",
        name: "gastos-por-departamento",
        component: () => import("@/views/core/DepartamentoGastosView.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "relatorios/despesas",
        name: "relatorio-despesas",
        component: () => import("@/views/core/RelatorioDespesasView.vue"),
        meta: { 
          requiresAuth: true,
          title: 'Relatório de Despesas'
        },
      },
    ],
  },
]
