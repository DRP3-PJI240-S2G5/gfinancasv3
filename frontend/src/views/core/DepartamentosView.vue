<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <!-- Título e Botão na mesma linha -->
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline" align="center">
                Departamentos
              </v-card-title>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-col v-for="item in departamentos" :key="item.id" cols="12">
        <f-departamento :departamento="item"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useCoreStore } from "@/stores/coreStore"
import FDepartamento from "@/components/FDepartamento.vue"

export default {
  name: "DepartamentosList",
  components: { FDepartamento },
  setup() {
    const baseStore = useBaseStore()
    const coreStore = useCoreStore()
    return { baseStore, coreStore }
  },
  data() {
    return {
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
