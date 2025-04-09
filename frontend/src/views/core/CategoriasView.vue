<template>
  <v-container class="fill-height">
    <v-row>
      <!-- COLUNA 1 - LISTA DE USUÁRIOS -->
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline">Elementos</v-card-title>
            </v-col>
            <v-col class="d-flex justify-end">
              <v-btn @click="toggleFormElemento" color="primary" fab small>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>

        <div v-if="showFormElemento" class="mb-4">
          <elemento-form :form-label="'Novo Elemento'" @new-elemento="addNewElemento" />
        </div>

        <div v-for="item in elementos" :key="item.id" class="mb-2">
          <elemento :elemento="item" />
        </div>
      </v-col>

      <!-- COLUNA 2 - LISTA DE USUÁRIOS (simulando outra entidade) -->
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline">Tipos de Gastos</v-card-title>
            </v-col>
          <v-col class="d-flex justify-end">
              <v-btn @click="toggleFormUser" color="primary" fab small>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>

        <div v-if="showFormUser" class="mb-4">
          <user-form :form-label="'Novo Usuario'" @new-user="addNewUser" />
        </div>

        <div v-for="item in users" :key="`col2-${item.id}`" class="mb-2">
          <user :user="item" />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useCoreStore } from "@/stores/coreStore"
import { useAccountsStore } from "@/stores/accountsStore"
import User from "@/components/User.vue"
import UserForm from "@/components/UserForm.vue"
import Elemento from "@/components/Elemento.vue"
import ElementoForm from "@/components/ElementoForm.vue"

export default {
  name: "UsersList",
  components: { User, UserForm, Elemento, ElementoForm },
  setup() {
    const baseStore = useBaseStore()
    const accountsStore = useAccountsStore()
    const coreStore = useCoreStore()
    return { baseStore, accountsStore, coreStore }
  },
  data() {
    return {
      showFormUser: false,
      showFormElemento: false,
    }
  },
  computed: {
    ...mapState(useAccountsStore, ["users", "usersLoading"]),
    ...mapState(useCoreStore, ["elementos", "elementosLoading"]),
  },
  mounted() {
    this.getUsers()
    this.getElementos()
  },
  methods: {
    getUsers() {
      this.accountsStore.getUsers()
    },
    async addNewUser(user) {
      const newUser = await this.accountsStore.addNewUser(user)
      this.baseStore.showSnackbar(`Novo usuário adicionado #${newUser.username}`)
      this.getUsers()
      this.showFormUser = !this.showFormUser;
    },
    toggleFormUser() {
      this.showFormUser = !this.showFormUser;
    },

    getElementos() {
      this.coreStore.getElementos()
    },
    async addNewElemento(elemento) {
      const newElemento = await this.coreStore.addNewElemento(elemento)
      this.baseStore.showSnackbar(`Novo elemento adicionado #${newElemento.elemento}`)
      this.getElementos()
      this.showFormElemento = !this.showFormElemento;
    },
    toggleFormElemento() {
      this.showFormElemento = !this.showFormElemento;
    },
  },
}
</script>

<style scoped>
.done {
  text-decoration: line-through;
}
</style>
