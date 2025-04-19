<template>
  <v-container>
    <v-card>
      <v-card-title class="text-overline">
        {{ departamento.nome }}

        <div class="text-green-darken-3 text-h3 font-weight-bold">90%</div>

        <div class="text-h6 text-medium-emphasis font-weight-regular">
          R$ 2.938,00 restante
        </div>
      </v-card-title>
      <br>
      <v-card-text>
        <div
          :style="`right: calc(${review} - 0px)`"
          class="position-absolute mt-n8 text-caption text-green-darken-3"
        >
          Meta
        </div>
        <v-progress-linear
          color="green-darken-3"
          height="22"
          model-value="90"
          rounded="lg"
        >
          <v-badge
            :style="`right: ${review}`"
            class="position-absolute"
            color="white"
            dot
            inline
          ></v-badge>
        </v-progress-linear>

        <div class="d-flex justify-space-between py-3">
          <span class="text-green-darken-3 font-weight-medium">
            R$ 26.442,00<br>gastos e despesas
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
    itensPorPagina: 10
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
