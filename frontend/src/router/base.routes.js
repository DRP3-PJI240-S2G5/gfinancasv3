// Composables
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"
import HomeView from "@/views/base/HomeView.vue"
import GetStartedView from "@/views/base/GetStartedView.vue"
import InitialView from "@/views/base/InitialView.vue"

export default [
  {
    path: "/",
    component: DefaultLayout,
    children: [
      {
        path: "",
        name: "base-home",
        component: HomeView,
      },
      {
        path: "inicial",
        name: "inicial",
        component: InitialView,
      },
      {
        path: "getstarted",
        name: "base-getstarted",
        component: GetStartedView,
      },
    ],
  },
]
