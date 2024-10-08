// Composables
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"
import InitialView from "@/views/core/InitialView.vue"

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
    ],
  },
]
