<template>
  <v-dialog
    v-model="dialog"
    max-width="400"
  >
    <v-card>
      <v-card-title class="text-h5">
        {{ title }}
      </v-card-title>

      <v-card-text>
        {{ message }}
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          variant="text"
          @click="cancel"
        >
          Cancelar
        </v-btn>
        <v-btn
          color="error"
          variant="text"
          @click="confirm"
        >
          Confirmar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ConfirmDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: 'Confirmar ação'
    },
    message: {
      type: String,
      required: true
    }
  },
  emits: ['update:modelValue', 'confirm', 'cancel'],
  computed: {
    dialog: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  },
  methods: {
    confirm() {
      this.$emit('confirm')
      this.dialog = false
    },
    cancel() {
      this.$emit('cancel')
      this.dialog = false
    }
  }
}
</script> 