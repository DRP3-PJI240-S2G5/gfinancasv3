<template>
  <v-card>
    <v-card-text>
      <v-text-field v-model="tipoGasto" label="Tipo de Gasto" outlined append-icon="fa-user" />
      <v-text-field v-model="descricao" label="descrição" required outlined append-icon="fa-user" />
      <!-- <v-select v-model="role" :items="roleOptions" label="Função" required outlined append-icon="fa-cogs" /> -->

      <v-btn color="primary" @click="addNewTipoGasto">Criar Tipo de Gasto</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    formLabel: {
      type: String,
      default: "Novo Tipo de Gasto",
    },
  },
  emits: ["newTipoGasto"],
  data: () => {
    return {
      tipoGasto: "",
      descricao: "",
    };
  },
  methods: {
    addNewTipoGasto() {
      const newTipoGasto = {
        tipoGasto: this.tipoGasto,
        descricao: this.descricao,
      };
      this.$emit("newTipoGasto", newTipoGasto);
      this.tipoGasto = "";
      this.descricao = "";
    },
  },
};
</script>

<style scoped></style>
