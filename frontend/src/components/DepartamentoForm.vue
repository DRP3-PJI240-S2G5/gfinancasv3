<template>
  <div>
    <v-card>
      <v-card-text>
        <v-text-field v-model="nome" :label="formLabel" required outlined append-icon="fa-pen"/>
        <v-text-field v-model="description" label="Descrição" required outlined append-icon="fa-pen" />
        <v-select v-model="tipoEntidade" :items="tipoEntidadeOptions" label="Tipo de Entidade" required outlined
          append-icon="fa-caret-down" />

        <v-select v-model="responsavelId" :items="mappedUsers" label="Responsável"
          item-text="title" item-value="id" outlined append-icon="fa-user" />
        
        <v-btn color="primary" @click="addNewDepartamento">Salvar Departamento</v-btn>

      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { useAccountsStore } from "@/stores/accountsStore";
import { onMounted, computed } from 'vue'
import { storeToRefs } from 'pinia'

export default {
  props: {
    formLabel: {
      type: String,
      default: "",
    },
    responsavelOptions: {
      type: Array,
      default: () => [],
    }
  },
  emits: ["newDepartamento"],
  setup() {
    const accountStore = useAccountsStore()
    const { users } = storeToRefs(accountStore)

    onMounted(() => {
      accountStore.getUsers() // Carrega os usuários ao montar o componente
    })
    // Mapeando o nome para title, garantindo que seja uma string
    const mappedUsers = computed(() => {
      return users.value.map(user => ({
        ...user,
        title: user.username, // Mapeando o nome para title
        id: user.id,
      }));
    });
    return {
      users, mappedUsers
    }
  },
  data: () => {
    return {
      nome: "",
      description: "",
      tipoEntidade: "",
      responsavelId: null,
      done: false,
      tipoEntidadeOptions: ["Tipo A", "Tipo B", "Tipo C"]
    }
  },

  methods: {
    addNewDepartamento() {
      const newDepartamento = {
        nome: this.nome,
        description: this.description,
        tipoEntidade: this.tipoEntidade,
        responsavelId: this.responsavelId || 1,
        done: this.done,
      };
      this.$emit("newDepartamento", newDepartamento);
      this.nome = ""
      this.description = ""
      this.tipoEntidade = ""
      this.responsavelId = null
      this.done = false
    },
  },
}
</script>

<style scoped></style>
