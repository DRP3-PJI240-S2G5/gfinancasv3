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
        
        <!-- Campo para selecionar departamentos subordinados -->
        <v-select
          v-model="departamentosSubordinados"
          :items="departamentosDisponiveis"
          label="Supervisor de"
          item-text="text"
          item-value="value"
          multiple
          chips
          outlined
        ></v-select>

        <!-- Campo para selecionar departamento superior -->
        <v-select
          v-model="departamentoSuperior"
          :items="departamentosDisponiveis"
          label="Subordinado a"
          item-text="text"
          item-value="value"
          outlined
        ></v-select>

        <v-btn color="primary" @click="addNewDepartamento">Salvar</v-btn>

      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { useAccountsStore } from "@/stores/accountsStore";
import { useCoreStore } from "@/stores/coreStore";
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
    const coreStore = useCoreStore()
    const { users } = storeToRefs(accountStore)
    const { departamentos } = storeToRefs(coreStore)

    onMounted(async () => {
      accountStore.getUsers() // Carrega os usuários ao montar o componente
      await coreStore.getDepartamentos()
    })
    // Mapeando o nome para title, garantindo que seja uma string
    const mappedUsers = computed(() => {
      return users.value.map(user => ({
        ...user,
        title: user.username, // Mapeando o nome para title
        id: user.id,
      }));
    });

    // Departamentos disponíveis para seleção
    const departamentosDisponiveis = computed(() => {
      return departamentos.value.map(dep => ({
        title: dep.nome,
        value: dep.id
      }));
    });

    return {
      users, mappedUsers, departamentosDisponiveis
    }
  },
  data: () => {
    return {
      nome: "",
      description: "",
      tipoEntidade: "",
      responsavelId: null,
      done: false,
      tipoEntidadeOptions: ["Tipo A", "Tipo B", "Tipo C"],
      departamentosSubordinados: [],
      departamentoSuperior: null,
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
      this.departamentosSubordinados = []
      this.departamentoSuperior = null
    },
  },
}
</script>

<style scoped></style>
