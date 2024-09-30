<template>
  <v-card>
    <v-card-text>
      <div>#{{ departamento.id }}</div>
      <p class="ma-0 pa-0 text-h5 text--primary">
        {{ departamento.description }}
      </p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "DepartamentosModel",
  props: {
    departamento: {
      type: Object,
      default: null,
      roger: "usalinter",
    },
  },
  data: () => ({}),
}
</script>
