// Composables
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"
import InitialView from "@/views/core/InitialView.vue"
import AdminView from "@/views/core/AdminView.vue"

export default [
  {
    path: "/inicial",
    component: DefaultLayout,
    children: [
      {
        path: "",
        name: "inicial",
        component: InitialView,
      },
      {
        path: "/inicial/administracao",
        name: "administracao",
        component: AdminView,
      },
    ],
  },
]
