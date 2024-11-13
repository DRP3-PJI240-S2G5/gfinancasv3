<template>
  <v-card>
    <v-card-text>
      <v-text-field v-model="first_name" label="Nome" outlined append-icon="fa-user" />
      <v-text-field v-model="username" label="username" required outlined append-icon="fa-user" />
      <v-text-field v-model="email" label="Email" outlined append-icon="fa-envelope" />
      <v-select v-model="role" :items="roleOptions" label="Função" required outlined append-icon="fa-cogs" />
      
      <v-text-field
        v-model="password"
        label="Senha"
        type="password"
        required
        outlined
        append-icon="fa-key"
      />
      
      <v-btn color="primary" @click="addNewUser">Criar Usuário</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    formLabel: {
      type: String,
      default: "Novo Usuário",
    },
  },
  emits: ["newUser"],
  data: () => {
    return {
      first_name: "",
      username: "",
      email: "",
      password: "", 
      role: "",
      roleOptions: ["Administrador", "Gestor", "Leitor"]
    };
  },
  methods: {
    addNewUser() {
      const newUser = {
        first_name: this.first_name,
        username: this.username,
        email: this.email,
        password: this.password, 
        role: this.role,
      };
      this.$emit("newUser", newUser);
      this.first_name = "";
      this.username = "";
      this.email = "";
      this.password = "";  // Limpa o campo de senha
      this.role = "";
    },
  },
};
</script>

<style scoped></style>
