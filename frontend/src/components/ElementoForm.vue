<template>
  <v-card>
    <v-card-text>
      <v-form ref="form" @submit.prevent="submit">
        <v-text-field 
          v-model="elementoForm.elemento" 
          label="Elemento" 
          outlined 
          append-icon="fa-user" 
          :rules="[v => !!v || 'Elemento é obrigatório']"
          required
          @keyup.enter="submit"
        />
        <v-text-field 
          v-model="elementoForm.descricao" 
          label="Descrição" 
          required 
          outlined 
          append-icon="fa-user"
          :rules="[v => !!v || 'Descrição é obrigatória']"
          @keyup.enter="submit"
        />

        <div class="d-flex justify-end">
          <v-btn 
            class="mr-2"
            @click="$emit('cancel')"
          >
            Cancelar
          </v-btn>
          <v-btn 
            color="primary" 
            type="submit"
          >
            {{ elemento?.id ? 'Atualizar' : 'Adicionar' }}
          </v-btn>
        </div>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ElementoForm',
  props: {
    formLabel: {
      type: String,
      required: true
    },
    elemento: {
      type: Object,
      default: null
    }
  },
  emits: ['new-elemento', 'update-elemento', 'cancel'],
  data() {
    return {
      elementoForm: {
        elemento: '',
        descricao: ''
      }
    }
  },
  watch: {
    elemento: {
      handler(newElemento) {
        if (newElemento) {
          this.elementoForm = { ...newElemento }
        } else {
          this.resetForm()
        }
      },
      immediate: true
    }
  },
  methods: {
    resetForm() {
      this.elementoForm = {
        elemento: '',
        descricao: ''
      }
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    },
    async submit() {
      if (!this.$refs.form.validate()) {
        return
      }

      if (this.elemento?.id) {
        this.$emit('update-elemento', { ...this.elementoForm, id: this.elemento.id })
      } else {
        this.$emit('new-elemento', this.elementoForm)
      }
      this.resetForm()
    }
  }
}
</script>

<style scoped></style>
