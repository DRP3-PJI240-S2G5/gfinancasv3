<template>
  <v-container class="mt-10">
    <v-row justify="center"><v-card-title class="text-h6 text-md-h5 text-lg-h4">Gastos e Despesas</v-card-title></v-row>
    <v-row justify="center">
      <v-col cols="4">
        <card-option cardOptionTitle="Gabinete Teste Secretário" cardOptionDescription="#" cardOptionLink="/gastos/gabsecretario">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Departamentos teste de Esportes" cardOptionDescription="#" cardOptionLink="/gastos/esportes">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Departamentos de Lazer" cardOptionDescription="#" cardOptionLink="/gastos/lazer">
        </card-option>
      </v-col>

      <v-col 
        v-for="item in departamentos" 
        :key="item.id" 
        cols="12"
      >
        <card-option 
          :cardOptionTitle="item.nome" 
          cardOptionDescription="#" 
          :cardOptionLink="`/gastos/${item.slug || item.id}`"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useCoreStore } from "@/stores/coreStore"
import CardOption from "@/components/CardOption.vue"

export default {
  name: "GastosView",
  components: { CardOption },
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
      this.coreStore.getDepartamentos();
    }
  },
}
</script>

<style scoped></style>