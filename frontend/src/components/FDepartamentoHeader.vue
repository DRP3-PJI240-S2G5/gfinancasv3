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
      <v-card-text>
        <div class="position-relative" style="height: 22px;">
          <!-- Barra do departamento principal -->
          <v-progress-linear
            :color="corBarraProgresso"
            height="22"
            :model-value="ultrapassouLimite ? (porcentagemGastosDepartamento / porcentagemGastos) * 100 : Math.min(porcentagemGastosDepartamento, 100)"
            rounded="lg"
            class="position-absolute w-100"
            style="z-index: 2;"
          ></v-progress-linear>
          
          <!-- Barra dos subordinados -->
          <v-progress-linear
            :color="corBarraProgressoSubordinados"
            height="22"
            :model-value="ultrapassouLimite ? 100 : Math.min(porcentagemGastosSubordinados + porcentagemGastosDepartamento, 100)"
            :style="ultrapassouLimite ? `margin-left: ${(porcentagemGastosDepartamento / porcentagemGastos) * 100}%; width: ${100 - (porcentagemGastosDepartamento / porcentagemGastos) * 100}%` : ''"
            :rounded="ultrapassouLimite ? 's-lg' : 'lg'"
            class="position-absolute"
            style="z-index: 1;"
          ></v-progress-linear>

          <!-- Indicador de Meta (Verba) -->
          <div v-if="ultrapassouLimite" class="position-absolute" :style="`left: ${Math.min(100, (100 / porcentagemGastos) * 100)}%`" style="z-index: 4;">
            <v-badge
              class="text-caption"
              dot
              inline
              style="z-index: 4;"
            ></v-badge>
            <div class="text-caption mt-n2" style="white-space: nowrap; transform: translateX(-50%); z-index: 4;">
              {{ formatarValor(verbaAtual.valor) }}
            </div>
          </div>
        </div>

        <div class="d-flex justify-space-between py-3">
          <span class="text-green-darken-3 font-weight-medium">
            {{ totalDespesas }}<br>
            <span class="text-caption" style="color: #d6ae02;">+ {{ totalDespesasSubordinados }} (subordinados)</span><br>
            <span v-if="totalDespesas && totalDespesasSubordinados" class="text-body-2">Total: {{ 
              (formatarValorMonetario(totalDespesas) + formatarValorMonetario(totalDespesasSubordinados)).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) 
            }}</span>
          </span>

          <span class="text-medium-emphasis">
            <div v-if="carregandoVerba" class="d-flex align-center">
              <v-progress-circular indeterminate size="20" width="2" class="mr-2"></v-progress-circular>
              Carregando verba...
            </div>
            <div v-else-if="verbaAtual" class="text-h6 font-weight-bold">
              {{ formatarValor(verbaAtual.valor) }}
              <div class="text-caption">Verba atual</div>
            </div>
            <div v-else class="text-body-2">
              Nenhuma verba definida para este ano
            </div>
          </span>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { useCoreStore } from "@/stores/coreStore"
import { mapState } from "pinia"
import { storeToRefs } from "pinia"

export default {
  data: () => ({ 
    totalDespesas: "R$ 0,00",
    totalDespesasSubordinados: "R$ 0,00",
    verbaAtual: null,
    carregandoVerba: false
  }),
  props: {
    departamento: {
      type: Object,
      required: true,
    }
  },
  computed: {
    ...mapState(useCoreStore, ["despesasLoading"]),
    porcentagemGastosDepartamento() {
      const valorTotal = this.formatarValorMonetario(this.totalDespesas)
      const verbaAtual = this.verbaAtual ? parseFloat(this.verbaAtual.valor) : 0
      return verbaAtual > 0 ? (valorTotal / verbaAtual) * 100 : 0
    },
    porcentagemGastosSubordinados() {
      const valorSubordinados = this.formatarValorMonetario(this.totalDespesasSubordinados)
      const verbaAtual = this.verbaAtual ? parseFloat(this.verbaAtual.valor) : 0
      return verbaAtual > 0 ? (valorSubordinados / verbaAtual) * 100 : 0
    },
    porcentagemGastos() {
      return this.porcentagemGastosDepartamento + this.porcentagemGastosSubordinados
    },
    valorRestante() {
      const valorTotal = this.formatarValorMonetario(this.totalDespesas)
      const valorSubordinados = this.formatarValorMonetario(this.totalDespesasSubordinados)
      const verbaAtual = this.verbaAtual ? parseFloat(this.verbaAtual.valor) : 0
      const restante = verbaAtual - (valorTotal + valorSubordinados)
      return restante.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },
    ultrapassouLimite() {
      return this.porcentagemGastos > 100
    },
    corBarraProgresso() {
      return this.ultrapassouLimite ? 'red-darken-4' : 'green-darken-3'
    },
    corBarraProgressoSubordinados() {
      return '#d6ae02'
    },
    // Retorna todos os departamentos subordinados (diretos e indiretos)
    todosDepartamentosSubordinados() {
      const subordinados = new Set()
      
      const buscarSubordinados = (deptId) => {
        const subordinadosDiretos = this.coreStore.subordinacoes
          .filter(s => s.superior.id === deptId)
          .map(s => s.subordinado)
        
        for (const sub of subordinadosDiretos) {
          subordinados.add(sub)
          buscarSubordinados(sub.id)
        }
      }
      
      buscarSubordinados(this.departamento.id)
      return Array.from(subordinados)
    }
  },
  watch: {
    'coreStore.subordinacoes': {
      handler() {
        this.carregarTotalDespesas()
      },
      deep: true
    },
    'departamento.id': {
      handler(newValue) {
        if (newValue) {
          this.carregarVerbaAtual()
        }
      }
    }
  },
  async mounted() {
    await this.carregarVerbaAtual()
    this.iniciarAtualizacaoPeriodica()
  },
  beforeUnmount() {
    this.pararAtualizacaoPeriodica()
  },
  methods: {
    formatarValorMonetario(valor) {
      return parseFloat(valor.replace(/\s/g, '').replace('R$', '').replace(/\./g, '').replace(',', '.'))
    },
    async carregarVerbaAtual() {
      this.carregandoVerba = true
      try {
        this.verbaAtual = await this.coreStore.getUltimaVerbaDepartamento(this.departamento.id)
      } catch (error) {
        console.error("Erro ao carregar verba:", error)
      } finally {
        this.carregandoVerba = false
      }
    },
    formatarValor(valor) {
      if (!valor) return 'R$ 0,00'
      return parseFloat(valor).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },
    iniciarAtualizacaoPeriodica() {
      if (this.intervaloAtualizacao) {
        clearInterval(this.intervaloAtualizacao)
      }
      this.intervaloAtualizacao = setInterval(() => {
        this.carregarTotalDespesas()
        this.carregarVerbaAtual()
      }, 30000)
    },
    pararAtualizacaoPeriodica() {
      if (this.intervaloAtualizacao) {
        clearInterval(this.intervaloAtualizacao)
      }
    },
    async carregarTotalDespesas() {
      try {
        // Carrega despesas do departamento principal
        const response = await this.coreStore.getTotalDespesasDepartamento(this.departamento.id)
        this.totalDespesas = response.total_despesas_formatado

        // Carrega as despesas dos subordinados
        let totalSubordinados = 0
        const subordinados = this.todosDepartamentosSubordinados
        
        if (subordinados.length > 0) {
          for (const dept of subordinados) {
            const responseSub = await this.coreStore.getTotalDespesasDepartamento(dept.id)
            const valorSub = this.formatarValorMonetario(responseSub.total_despesas_formatado)
            totalSubordinados += valorSub
          }
        }
        
        this.totalDespesasSubordinados = totalSubordinados.toLocaleString('pt-BR', {
          style: 'currency',
          currency: 'BRL'
        })
      } catch (error) {
        console.error("Erro ao carregar total de despesas:", error)
      }
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
