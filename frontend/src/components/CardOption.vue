<template>
  <v-card class="mx-auto card-option" max-width="400" hover link :to="cardOptionLink">
    <v-card-title>
      <v-icon class="mr-2" left>{{ cardOptionIcon }}</v-icon>
      <span class="headline"> {{ cardOptionTitle }} </span>
    </v-card-title>
    <v-card-text>
      {{ cardOptionDescription }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'CardOption',
  props: {
    cardOptionTitle: {
      type: String,
      required: true
    },
    cardOptionDescription: {
      type: String,
      required: true
    },
    cardOptionLink: {
      type: String,
      required: true
    },
    cardOptionIcon: {
      type: String, // Adicionando a propriedade para o ícone
      required: false,
      default: 'mdi-information' // Definindo um ícone padrão
    }
  }
}
</script>
<style scoped></style>
