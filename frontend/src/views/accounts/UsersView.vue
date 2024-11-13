<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline">
                Usuários
              </v-card-title>
            </v-col>
            <v-col class="d-flex justify-end">
              <v-btn @click="toggleForm" color="primary" fab small>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-col cols="12" v-if="showForm">
        <user-form :form-label="'Novo Usuário'" @new-user="addNewUser" />
      </v-col>

      <v-col v-for="item in users" :key="item.id" cols="12">
        <user :user="item"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useAccountsStore } from "@/stores/accountsStore"
import User from "@/components/User.vue"
import UserForm from "@/components/UserForm.vue"

export default {
  name: "UsersList",
  components: { User, UserForm },
  setup() {
    const baseStore = useBaseStore()
    const accountsStore = useAccountsStore()
    return { baseStore, accountsStore }
  },
  data() {
    return {
      showForm: false,
    }
  },
  computed: {
    ...mapState(useAccountsStore, ["users", "usersLoading"]),
  },
  mounted() {
    this.getUsers()
  },
  methods: {
    getUsers() {
      this.accountsStore.getUsers()
    },
    async addNewUser(user) {
      const newUser = await this.accountsStore.addNewUser(user)
      this.baseStore.showSnackbar(`Novo usuário adicionado #${newUser.username}`)
      this.getUsers()
      this.showForm = !this.showForm;
    },
    toggleForm() {
      this.showForm = !this.showForm;
    },
  },
}
</script>

<style scoped>
.done {
  text-decoration: line-through;
}
</style>
