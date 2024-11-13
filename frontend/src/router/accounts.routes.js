// Composables
import EmptyLayout from "@/layouts/default/EmptyLayout.vue"
import LoginView from "@/views/accounts/LoginView.vue"
import LogoutView from "@/views/accounts/LogoutView.vue"
import UsersView from "@/views/accounts/UsersView.vue"
import DefaultLayout from "@/layouts/default/DefaultLayout.vue"

export default [
  {
    path: "/accounts",
    component: EmptyLayout,
    children: [
      {
        path: "login",
        name: "accounts-login",
        component: LoginView,
      },
      {
        path: "logout",
        name: "accounts-logout",
        component: LogoutView,
      },
    ],
  },
  {
    component: DefaultLayout,
    children: [
      {
        path: "/gestao/usuarios",
        name: "usuarios",
        component: UsersView,
        meta: { requiresAuth: true },
      },
    ]
  }
]
