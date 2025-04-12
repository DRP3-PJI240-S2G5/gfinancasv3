<template>
  <v-container class="mt-10">
    <v-row justify="center"><v-card-title class="text-h6 text-md-h5 text-lg-h4">Gastos e Despesas</v-card-title></v-row>
    <v-row justify="center">
      <v-col
        v-for="item in departamentos"
        :key="item.id"
        cols="12"
        sm="6"
        md="4">
        <card-option
          :cardOptionTitle="item.nome"
          cardOptionDescription="$"
          cardOptionIcon="mdi-plus"
          :cardOptionLink="`/gastos/${item.id}`"
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
