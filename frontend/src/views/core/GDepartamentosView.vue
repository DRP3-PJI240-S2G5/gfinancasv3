<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <!-- Título e Botão na mesma linha -->
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline">
                Departamentos
              </v-card-title>
            </v-col>
            <!-- Botão "+" posicionado no canto direito -->
            <v-col class="d-flex justify-end">
              <v-btn @click="toggleForm" color="primary" fab small>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-col cols="12" v-if="showForm">
        <departamento-form :form-label="'Novo Departamento'" @new-departamento="addNewDepartamento" />
      </v-col>

      <v-col v-for="item in departamentos" :key="item.id" cols="12">
        <departamento :departamento="item" @updateDepartamento="updateDepartamento" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useCoreStore } from "@/stores/coreStore"
import Departamento from "@/components/Departamento.vue"
import DepartamentoForm from "@/components/DepartamentoForm.vue"

export default {
  name: "GDepartamentosList",
  components: { Departamento, DepartamentoForm },
  setup() {
    const baseStore = useBaseStore()
    const coreStore = useCoreStore()
    return { baseStore, coreStore }
  },
  data() {
    return {
      showForm: false, // Variável para controlar a visibilidade do formulário
    }
  },
  computed: {
    ...mapState(useCoreStore, ["departamentos", "departamentosLoading"]),
  },
  mounted() {
    this.getDepartamentos()
  },
  methods: {
    getDepartamentos() {
      this.coreStore.getDepartamentos()
    },
    async addNewDepartamento(departamento) {
      const newDepartamento = await this.coreStore.addNewDepartamento(departamento)
      this.baseStore.showSnackbar(`Novo departamento adicionado #${newDepartamento.id}`)
      this.getDepartamentos()
      this.showForm = !this.showForm;
    },
    async updateDepartamento(updatedDepartamento) {
      await this.coreStore.updateDepartamento(updatedDepartamento)
      this.baseStore.showSnackbar(`Departamento #${updatedDepartamento.id} atualizado  com sucesso`)
      this.getDepartamentos()
    },
    toggleForm() {
      this.showForm = !this.showForm; // Alterna a visibilidade do formulário
    },
  },
}
</script>

<style scoped>
@font-face {
  font-family: 'Material Design Icons';
  src: url('/node_modules/@mdi/font/fonts/materialdesignicons-webfont.woff2?v=7.0.96') format('woff2');
  font-display: swap;
}

.done {
  text-decoration: line-through;
}
</style>
