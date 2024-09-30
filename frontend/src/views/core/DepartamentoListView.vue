<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline"> Departamentos </v-card-title>
        </v-card>
      </v-col>

      <v-col cols="12">
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
import { usecoreStore } from "@/stores/coreStore"
import Departamento from "@/components/Departamento.vue"
import DepartamentoForm from "@/components/DepartamentoForm.vue"

export default {
  name: "DepartamentosList",
  components: { Departamento, DepartamentoForm },
  setup() {
    const baseStore = useBaseStore()
    const coreStore = usecoreStore()
    return { baseStore, coreStore }
  },
  computed: {
    ...mapState(usecoreStore, ["departamentos", "departamentosLoading"]),
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
  },
}
</script>

<style scoped>
.done {
  text-decoration: line-through;
}
</style>
