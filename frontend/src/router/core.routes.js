// Composables
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"
import AdminView from "@/views/core/AdminView.vue"
import GastosView from "@/views/core/GastosView.vue"

export default [
  {
    path: "/",
    component: DefaultLayout,
    children: [
      {
        path: "gastos",
        name: "gastos",
        component: GastosView,
      },
      {
        path: "gestao",
        name: "gestao",
        component: AdminView,
      },
    ],
  },
]
