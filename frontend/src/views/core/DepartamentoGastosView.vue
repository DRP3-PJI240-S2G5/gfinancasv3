<template>
  <v-container class="mt-10">
    <v-card>
      <v-card-title>
        Lançar Gasto - {{ departamento?.nome || 'Departamento' }}
      </v-card-title>
      <v-card-text>
        <!-- Formulário de lançamento vai aqui -->
        <p>Formulário de lançamento virá aqui...</p>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useCoreStore } from "@/stores/coreStore"

export default {
  name: "DepartamentoGastosView",
  computed: {
    ...mapState(useCoreStore, ["departamentos"]),
    departamento() {
      const id = this.$route.params.departamento
      return this.departamentos.find(
        dep => dep.id === id || dep.id.toString() === id
      )
    },
  },
  mounted() {
    // Se ainda não tiver carregado os departamentos, pode forçar aqui
    if (!this.departamentos.length) {
      this.$pinia._s.get("coreStore").getDepartamentos()
    }
  },
}
</script>

<style scoped></style>
