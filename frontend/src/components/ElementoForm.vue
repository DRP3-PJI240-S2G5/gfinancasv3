<template>
  <v-card>
    <v-card-text>
      <v-text-field v-model="elemento" label="Elemento" outlined append-icon="fa-user" />
      <v-text-field v-model="descricao" label="descricao" required outlined append-icon="fa-user" />
      <!-- <v-select v-model="role" :items="roleOptions" label="Função" required outlined append-icon="fa-cogs" /> -->

      <v-btn color="primary" @click="addNewElemento">Criar Elemento</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    formLabel: {
      type: String,
      default: "Novo Elemento",
    },
  },
  emits: ["newElemento"],
  data: () => {
    return {
      elemento: "",
      descricao: "",
    };
  },
  methods: {
    addNewElemento() {
      const newElemento = {
        elemento: this.elemento,
        descricao: this.descricao,
      };
      this.$emit("newElemento", newElemento);
      this.elemento = "";
      this.descricao = "";
    },
  },
};
</script>

<style scoped></style>
