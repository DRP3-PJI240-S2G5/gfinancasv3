<template>
  <v-container class="mt-10">
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
              <v-btn
                @click="toggleForm"
                color="primary"
                fab
                small>
              <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-col cols="12" v-if="showForm">
        <departamento-form :form-label="'New Departamento'" @new-departamento="addNewDepartamento" />
      </v-col>

      <v-col v-for="item in departamentos" :key="item.id" cols="12">
        <departamento :departamento="item" />
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
  name: "DepartamentosView",
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
      this.baseStore.showSnackbar(`New departamento added #${ newDepartamento.id }`)
      this.getDepartamentos()
    },
    toggleForm() {
      this.showForm = !this.showForm; // Alterna a visibilidade do formulário
    },
  },
}
</script>

<style scoped>
.done {
  text-decoration: line-through;
}
</style>
