<template>
  <v-container class="mt-10">
    <v-card>
      <v-card-title class="text-h5">Consulta de Leis e Normas</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item v-for="lei in leis" :key="lei.id">
            <v-list-item-content>
              <v-list-item-title>{{ lei.numero }} - {{ lei.titulo }}</v-list-item-title>
              <v-list-item-subtitle>{{ formatarData(lei.data_publicacao) }} - {{ lei.descricao }}</v-list-item-subtitle>
              <v-btn v-if="lei.arquivo" :href="lei.arquivo" target="_blank" text color="primary">Ver Arquivo</v-btn>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'LeisNormasView',
  data() {
    return {
      leis: []
    }
  },
  methods: {
    formatarData(dataString) {
      const data = new Date(dataString);
      return data.toLocaleDateString('pt-BR');
    }
  },
  mounted() {
    fetch('/api/core/leis-normas/')
      .then(res => res.json())
      .then(data => {
        this.leis = data.leis_normas;
      })
      .catch(() => {
        alert('Erro ao carregar leis e normas.');
      })
  }
}
</script>

