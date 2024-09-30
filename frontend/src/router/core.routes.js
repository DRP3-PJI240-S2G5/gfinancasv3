// Composables
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"
import DepartamentoListView from "@/views/core/DepartamentoListView.vue"

export default [
  {
    path: "/departamentos",
    component: DefaultLayout,
    children: [
      {
        path: "list",
        name: "departamentos-list",
        component: DepartamentoListView,
      },
    ],
  },
]
