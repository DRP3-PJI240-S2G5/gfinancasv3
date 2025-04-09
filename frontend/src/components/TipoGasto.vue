<template>
  <v-card>
    <v-card-text>
      <span class="ma-0 pa-0 text-h6" >
        {{tipoGasto.id}}: {{ tipoGasto.tipoGasto }}
      </span>
      <p></p>

      <span class="ma-0 pa-0 text-h6" >
        Descrição: {{ tipoGasto.descricao }}
      </span>
    </v-card-text>

    <v-card-actions>
      <v-btn color="primary">Excluir</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    tipoGasto: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped></style>
