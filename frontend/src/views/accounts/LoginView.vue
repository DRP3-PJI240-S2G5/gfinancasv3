<template>
  <v-container>
    <v-row align="center" class="mt-10" no-gutters>
      <v-col cols="12" sm="6" offset-sm="3">
        <v-sheet class="pa-2"> <h1>Login</h1> </v-sheet>
        <v-form>
          <v-text-field
            v-model="username"
            label="username"
            prepend-inner-icon="mdi-account"
            variant="outlined"
            required
            @keyup.enter="login"></v-text-field>

          <v-text-field
            v-model="password"
            type="password"
            label="Password"
            prepend-inner-icon="mdi-key-outline"
            variant="outlined"
            required
            @keyup.enter="login"></v-text-field>

          <v-btn
            block
            size="large"
            rounded="pill"
            color="#038C4C"
            append-icon="mdi-chevron-right"
            @click="login">
            Login
          </v-btn>
          <v-btn
            class="my-2"
            block
            size="large"
            rounded="pill"
            color="#038C4C"
            variant="outlined"
            :to="{ name: 'base-home' }">
            Início
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useAccountsStore } from "@/stores/accountsStore"

export default {
  setup() {
    const baseStore = useBaseStore()
    const accountsStore = useAccountsStore()
    return { baseStore, accountsStore }
  },
  data: () => {
    return {
      valid: false,
      username: "",
      password: "",
    }
  },
  computed: {
    ...mapState(useAccountsStore, ["loggedUser"]),
  },
  async mounted() {
    console.log(this.loggedUser)
    await this.accountsStore.whoAmI()
    if (this.loggedUser) {
      this.baseStore.showSnackbar("Usuário já logado", "warning")
      this.showInicial()
    }
  },
  methods: {
    async login() {
      const user = await this.accountsStore.login(this.username, this.password)
      if (!user) {
        this.baseStore.showSnackbar("Usuário ou senha invalida", "danger")
        return
      }
      console.log("logged")
      this.showInicial()
    },
    showInicial() {
      this.$router.push({ name: "inicial" })
      console.log("--> inicial")
    },
  },
}
</script>
