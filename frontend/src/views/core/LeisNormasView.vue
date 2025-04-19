<template>
  <v-container class="mt-10">
    <v-card>
      <v-card-title class="text-h5">Consulta de Leis e Normas</v-card-title>
      <v-card-text>
        <v-progress-linear
          v-if="leisNormasLoading"
          indeterminate
          color="primary"
        ></v-progress-linear>
        <v-list v-else>
          <v-list-item v-for="lei in leisNormas" :key="lei.id">
            <v-list-item-title>{{ lei.numero }} - {{ lei.titulo }}</v-list-item-title>
            <v-list-item-subtitle>{{ formatarData(lei.data_publicacao) }} - {{ lei.descricao }}</v-list-item-subtitle>
            <template v-slot:append>
              <v-btn v-if="lei.arquivo" :href="lei.arquivo" target="_blank" text color="primary">Ver Arquivo</v-btn>
            </template>
          </v-list-item>
        </v-list>
        <v-alert v-if="!leisNormasLoading && leisNormas.length === 0" type="info" class="mt-2">
          Nenhuma lei ou norma cadastrada.
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { useCoreStore } from "@/stores/coreStore"
import { useBaseStore } from "@/stores/baseStore"
import { mapState } from "pinia"

export default {
  name: 'LeisNormasView',
  setup() {
    const coreStore = useCoreStore()
    const baseStore = useBaseStore()
    return { coreStore, baseStore }
  },
  computed: {
    ...mapState(useCoreStore, ["leisNormas", "leisNormasLoading"]),
  },
  methods: {
    formatarData(dataString) {
      const data = new Date(dataString);
      return data.toLocaleDateString('pt-BR');
    }
  },
  async mounted() {
    try {
      await this.coreStore.getLeisNormas();
    } catch (error) {
      this.baseStore.showSnackbar("Erro ao carregar leis e normas.");
    }
  }
}
</script> 