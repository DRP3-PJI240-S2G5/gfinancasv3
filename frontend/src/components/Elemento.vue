<template>
  <v-card>
    <v-card-text>
      <span class="ma-0 pa-0 text-h6" >
        Elemento: {{ elemento.elemento }}
      </span>
      <p></p>

      <span class="ma-0 pa-0 text-h6" >
        Descrição: {{ elemento.descricao }}
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
    elemento: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped></style>
