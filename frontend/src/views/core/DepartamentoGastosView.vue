<template>
  <v-container class="fill-height mt-10">
    <v-row justify="center">
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            Lançar Gasto - {{ departamento?.nome || 'Departamento' }}
          </v-card-title>

          <v-card-text>
            <v-form ref="form" @submit.prevent="lancarGasto">
              <v-text-field
                v-model="valorFormatado"
                label="Valor do Gasto"
                type="text"
                prefix="R$"
                required
                @blur="formatarValor"
              />

              <v-select
                v-model="elementoSelecionado"
                :items="elementos"
                item-title="elemento"
                item-value="id"
                label="Elemento"
                @update:modelValue="carregarTiposGasto"
                :loading="elementosLoading"
                required
              />

              <v-select
                v-model="tipoGastoSelecionado"
                :items="tipoGastosDisponiveis"
                item-title="tipoGasto"
                item-value="id"
                label="Tipo de Gasto"
                :disabled="!elementoSelecionado"
                required
              />

              <v-btn type="submit" color="primary" class="mt-4">Lançar</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useCoreStore } from "@/stores/coreStore"
import { useBaseStore } from "@/stores/baseStore"
import { mapState } from "pinia"

export default {
  name: "DepartamentoGastosView",
  setup() {
    const coreStore = useCoreStore()
    const baseStore = useBaseStore()
    return { coreStore, baseStore }
  },
  data() {
    return {
      valor: null,
      valorFormatado: '',
      elementoSelecionado: null,
      tipoGastoSelecionado: null,
      tipoGastosDisponiveis: [],
    }
  },
  computed: {
    ...mapState(useCoreStore, ["departamentos", "elementos", "elementosLoading"]),
    departamento() {
      const id = this.$route.params.departamento
      return this.departamentos.find(dep => dep.id === id || dep.id.toString() === id)
    },
  },
  mounted() {
    if (!this.departamentos.length) this.coreStore.getDepartamentos()
    if (!this.elementos.length) this.coreStore.getElementos()
  },
  methods: {
    async carregarTiposGasto() {
      try {
        const tipos = await this.coreStore.getTipoGastosPorElemento(this.elementoSelecionado)
        console.log("Tipos de gasto recebidos:", tipos)
        this.tipoGastosDisponiveis = tipos
        this.tipoGastoSelecionado = null
      } catch (error) {
        console.error("Erro ao carregar tipos de gasto:", error)
        this.baseStore.showSnackbar("Erro ao carregar os tipos de gasto.")
      }
    },
    formatarValor() {
      // Converte string com vírgula para número com ponto
      const numerico = parseFloat(this.valorFormatado.replace(',', '.'))
      if (!isNaN(numerico)) {
        this.valor = numerico
      } else {
        this.valor = null
      }
    },
    async lancarGasto() {
      this.formatarValor()
      if (!this.valor || !this.elementoSelecionado || !this.tipoGastoSelecionado) {
        this.baseStore.showSnackbar("Preencha todos os campos corretamente!")
        return
      }

      const payload = {
        valor: this.valor,
        elemento_id: this.elementoSelecionado,
        tipo_gasto_id: this.tipoGastoSelecionado,
        departamento_id: this.departamento.id,
      }

      console.log("Lançamento de gasto:", payload)
      this.baseStore.showSnackbar("Gasto lançado com sucesso!")

      // Resetar formulário
      this.valor = null
      this.valorFormatado = ''
      this.elementoSelecionado = null
      this.tipoGastosDisponiveis = []
      this.tipoGastoSelecionado = null
    },
  },
}
</script>

<style scoped></style>
