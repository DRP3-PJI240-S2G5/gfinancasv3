<template>
  <div>
    <v-card>
      <v-card-text>
        <v-text-field
          v-model="title"
          :label="formLabel"
          required
          outlined
          append-icon="fa-pen"
          @keyup.enter="addNewDepartamento" />
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    formLabel: {
      type: String,
      default: "",
    },
  },
  emits: ["newDepartamento"],
  data: () => {
    return {
      title: "",
    }
  },
  methods: {
    addNewDepartamento() {
      this.$emit("newDepartamento", {
        title: this.title,
      })
      this.title = ""
    },
  },
}
</script>

<style scoped></style>
