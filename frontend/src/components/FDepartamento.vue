<template>
  <v-container>
    <v-card>
      <v-card-title class="text-overline">
        {{ departamento.nome }}

        <div :class="`text-${corBarraProgresso} text-h3 font-weight-bold`">{{ Math.round(porcentagemGastos) }}%</div>

        <div class="text-h6 text-medium-emphasis font-weight-regular">
          {{ valorRestante }} {{ ultrapassouLimite ? 'excedido' : 'restante' }}
        </div>
      </v-card-title>
      <br>
      <v-card-text>
        <div
          :style="`right: calc(${Math.min(porcentagemGastos, 100)}% - 0px)`"
          class="position-absolute mt-n8 text-caption"
          :class="`text-${corBarraProgresso}`"
        >
          Meta
        </div>
        <v-progress-linear
          :color="corBarraProgresso"
          height="22"
          :model-value="Math.min(porcentagemGastos, 100)"
          rounded="lg"
        >
          <v-badge
            :style="`right: ${Math.min(porcentagemGastos, 100)}%`"
            class="position-absolute"
            color="white"
            dot
            inline
          ></v-badge>
        </v-progress-linear>

        <div class="d-flex justify-space-between py-3">
          <span class="text-green-darken-3 font-weight-medium">
            {{ totalDespesas }}<br>gastos e despesas
          </span>

          <span class="text-medium-emphasis"> R$ 29.380,00<br>verba total </span>
        </div>
      </v-card-text>

      <v-divider></v-divider>

      <v-list-item
        append-icon="mdi-chevron-right"
        lines="two"
        subtitle="Detalhes"
        link
        @click="toggleDetails"
      ></v-list-item>

      <v-expand-transition>
        <div v-show="isActive" class="smooth-transition">
          <v-progress-linear
            v-if="despesasLoading"
            indeterminate
            color="primary"
          ></v-progress-linear>
          <div v-else>
            <v-list dense>
              <template v-if="despesas.length">
                <v-list-item
                  v-for="despesa in despesas"
                  :key="despesa.id"
                >
                  <v-list-item-title>{{ despesa.justificativa }}</v-list-item-title>
                  <v-list-item-subtitle>
                    R$ {{ formatarValor(despesa.valor) }} - {{ formatarData(despesa.created_at) }}
                  </v-list-item-subtitle>
                </v-list-item>
              </template>
              <v-list-item v-else>
                <v-list-item-title class="text-medium-emphasis">
                  Nenhuma despesa registrada
                </v-list-item-title>
              </v-list-item>
            </v-list>

            <!-- Paginação -->
            <v-pagination
              v-if="totalPaginas > 1"
              v-model="paginaAtual"
              :length="totalPaginas"
              :total-visible="5"
              class="mt-4"
              @update:model-value="mudarPagina"
            ></v-pagination>
          </div>
        </div>
      </v-expand-transition>
    </v-card>
  </v-container>
</template>

<script>
import { useCoreStore } from "@/stores/coreStore"
import { mapState } from "pinia"

export default {
  data: () => ({ 
    review: "30%",
    despesas: [],
    paginaAtual: 1,
    totalPaginas: 1,
    itensPorPagina: 10,
    totalDespesas: "R$ 0,00",
    verbaTotal: 29380.00,
    intervaloAtualizacao: null
  }),
  props: {
    departamento: {
      type: Object,
      required: true,
    },
    isActive: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    ...mapState(useCoreStore, ["despesasLoading"]),
    porcentagemGastos() {
      // Extrai o valor numérico do totalDespesas (remove "R$ " e converte vírgula para ponto)
      const valorTotal = parseFloat(this.totalDespesas.replace('R$ ', '').replace('.', '').replace(',', '.'))
      // Calcula a porcentagem
      return (valorTotal / this.verbaTotal) * 100
    },
    valorRestante() {
      // Extrai o valor numérico do totalDespesas
      const valorTotal = parseFloat(this.totalDespesas.replace('R$ ', '').replace('.', '').replace(',', '.'))
      // Calcula o valor restante
      const restante = this.verbaTotal - valorTotal
      // Formata o valor restante
      return restante.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },
    ultrapassouLimite() {
      return this.porcentagemGastos > 100
    },
    corBarraProgresso() {
      return this.ultrapassouLimite ? 'red-darken-3' : 'green-darken-3'
    }
  },
  watch: {
    isActive: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.carregarDespesas()
        }
      }
    }
  },
  mounted() {
    this.carregarTotalDespesas()
    // Inicia o polling a cada 30 segundos
    this.intervaloAtualizacao = setInterval(() => {
      this.carregarTotalDespesas()
    }, 30000) // 30 segundos
  },
  beforeUnmount() {
    // Limpa o intervalo quando o componente for desmontado
    if (this.intervaloAtualizacao) {
      clearInterval(this.intervaloAtualizacao)
    }
  },
  methods: {
    toggleDetails() {
      this.$emit("toggle-department", this.departamento.id);
    },
    async carregarDespesas() {
      try {
        const response = await this.coreStore.getDespesasPorDepartamento(
          this.departamento.id, 
          this.paginaAtual, 
          this.itensPorPagina
        )
        this.despesas = response.despesas
        this.totalPaginas = response.totalPaginas
      } catch (error) {
        console.error("Erro ao carregar despesas:", error)
      }
    },
    async carregarTotalDespesas() {
      try {
        const response = await this.coreStore.getTotalDespesasDepartamento(this.departamento.id)
        this.totalDespesas = response.total_despesas_formatado
      } catch (error) {
        console.error("Erro ao carregar total de despesas:", error)
      }
    },
    async mudarPagina(novaPagina) {
      this.paginaAtual = novaPagina
      await this.carregarDespesas()
    },
    formatarValor(valor) {
      return parseFloat(valor).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    },
    formatarData(dataString) {
      const data = new Date(dataString)
      return data.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  },
  setup() {
    const coreStore = useCoreStore()
    return { coreStore }
  }
};
</script>

<style scoped>
.smooth-transition {
  transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}
</style>
