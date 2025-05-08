<template>
  <v-card>
    <v-card-text>
      <v-text-field 
        v-model="tipoGasto" 
        label="Tipo de Gasto" 
        outlined 
        append-icon="mdi-currency-usd" 
      />
      <v-text-field 
        v-model="descricao" 
        label="Descrição" 
        required 
        outlined 
        append-icon="mdi-text" 
      />
      <!-- <v-select v-model="role" :items="roleOptions" label="Função" required outlined append-icon="fa-cogs" /> -->

      <v-btn 
        color="primary" 
        @click="addTipoGasto"
        :disabled="!tipoGasto || !descricao || !elementoId"
      >
        Adicionar
      </v-btn>
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
    elementoId: {
      type: [Number, String],
      required: true
    }
  },
  emits: ["newTipoGasto"],
  data: () => {
    return {
      tipoGasto: "",
      descricao: "",
    };
  },
  methods: {
    addTipoGasto() {
      const newTipoGasto = {
        tipoGasto: this.tipoGasto,
        descricao: this.descricao,
        elemento_id: this.elementoId
      };
      this.$emit("newTipoGasto", newTipoGasto);
      this.tipoGasto = "";
      this.descricao = "";
    },
  },
};
</script>

<style scoped></style>
