<template>
  <v-card>
    <v-card-text>
      <div>#{{ user.id }}</div>
      
      <span class="ma-0 pa-0 text-h6" >
        Nome: {{ user.first_name }}
      </span>
      <p></p>

      <span class="ma-0 pa-0 text-h6" >
        username: {{ user.username }}
      </span>
      <p></p>
      <span class="ma-0 pa-0 text-h6" >
        Email: {{ user.email }}
      </span>
      <p></p>
      <span class="ma-0 pa-0 text-h6" >
        Grupo: {{ user.grupo }}
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
    user: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped></style>
