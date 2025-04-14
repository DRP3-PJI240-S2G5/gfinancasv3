<template>
  <v-container class="mt-10">
    <v-row justify="center">
  <!-- Coluna do formulário (formulário de lançamento de gasto) -->
  <v-col cols="12" md="8">
    <v-card>
      <v-card-title class="headline">
        Lançar Gasto - {{ departamento?.nome || 'Departamento' }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" @submit.prevent="lancarGasto">
          <!-- Campos do formulário -->
          <v-text-field
            v-model="valorFormatado"
            label="Valor do Gasto"
            type="text"
            prefix="R$"
            required
            @input="validarEntradaValor"
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
          <v-textarea
            v-model="justificativa"
            label="Justificativa"
            rows="3"
            auto-grow
            required
          />
          <v-btn type="submit" color="primary" class="mt-4">{{ modoEdicao ? 'Atualizar' : 'Lançar' }}</v-btn>
          <v-btn v-if="modoEdicao" color="secondary" class="mt-4 ml-2" @click="cancelarEdicao">Cancelar</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-col>

  <!-- Coluna de despesas recentes (do lado direito) -->
  <v-col cols="12" md="4">
    <v-card>
      <v-card-title class="headline">
        Despesas Recentes
      </v-card-title>
      <v-card-text>
        <v-list>
          <template v-if="despesas.length">
            <v-list-item
              v-for="despesa in despesas"
              :key="despesa.id"
              class="flex-column align-start"
            >
              <div class="d-flex justify-space-between align-center w-100">
                <span class="text-body-1 font-weight-medium">
                  R$ {{ formatarValorExibicao(despesa.valor) }} - {{ despesa.justificativa }}
                </span>
                <div class="d-flex">
                  <v-btn
                    v-if="podeEditarDespesa(despesa)"
                    color="primary"
                    size="small"
                    icon
                    class="mr-2"
                    @click="editarDespesa(despesa)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn
                    v-if="podeDeletarDespesa(despesa)"
                    color="error"
                    size="small"
                    icon
                    @click="deletarDespesa(despesa.id)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </div>
              </div>
              <span class="text-caption text-grey-darken-1">
                {{ " " }} {{ formatarData(despesa.created_at) }}
              </span>
            </v-list-item>
          </template>

          <v-alert v-else type="info" class="mt-2">
            Nenhuma despesa registrada. 
          </v-alert>
        </v-list>
        <!-- Paginação -->
        <v-pagination
          v-if="totalPaginas > 1"
          v-model="despesasPage"
          :length="totalPaginas"
          :total-visible="5"
          class="mt-4"
          @update:modelValue="carregarDespesas"
        />
      </v-card-text>
    </v-card>
  </v-col>
</v-row>
  </v-container>
</template>

<script>
import { useCoreStore } from "@/stores/coreStore"
import { useBaseStore } from "@/stores/baseStore"
import { useAccountsStore } from "@/stores/accountsStore"
import { mapState } from "pinia"

export default {
  name: "DepartamentoGastosView",
  setup() {
    const coreStore = useCoreStore()
    const baseStore = useBaseStore()
    const accountsStore = useAccountsStore()
    return { coreStore, baseStore, accountsStore }
  },
  data() {
    return {
      valor: null,
      valorFormatado: '',
      elementoSelecionado: null,
      tipoGastoSelecionado: null,
      tipoGastosDisponiveis: [],
      justificativa: '',
      despesas: [],
      despesasPage: 1,  // Controla a página atual das despesas
      perPage: 10,  // Número de despesas por página
      totalPaginas: 1,
      modoEdicao: false,
      despesaEmEdicao: null,
    }
  },
  computed: {
    ...mapState(useCoreStore, ["departamentos", "elementos", "elementosLoading"]),
    departamento() {
      const id = this.$route.params.departamento
      console.log('ID do departamento na URL:', id);
      return this.departamentos.find(dep => dep.id === id || dep.id.toString() === id)
    },
  },
  watch: {
    departamentos: {
      handler(novosDepartamentos) {
        if (novosDepartamentos.length && this.departamento) {
          this.carregarDespesas(1)
        }
      },
      immediate: true,
    },
  },
  mounted() {
    if (!this.departamentos.length) this.coreStore.getDepartamentos()
    if (!this.elementos.length) this.coreStore.getElementos()
  },
  methods: {
    validarEntradaValor(event) {
      const valor = event.target.value;
      // Remove todos os caracteres que não são números, ponto ou vírgula
      const valorLimpo = valor.replace(/[^\d.,]/g, '');
      
      // Se houver alteração, atualiza após 300ms
      if (valorLimpo !== valor) {
        setTimeout(() => {
          this.valorFormatado = valorLimpo;
        }, 300);
      }
    },
    formatarValorExibicao(valor) {
      // Converte para número caso seja string
      const numero = typeof valor === 'string' ? parseFloat(valor) : valor;
      // Verifica se é um número válido
      if (isNaN(numero)) return '0,00';
      return numero.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    async carregarDespesas(page = 1) {
      try {
        const resultado = await this.coreStore.getDespesasPorDepartamento(this.departamento.id, page, this.perPage)
        console.log("Despesas carregadas:", resultado.despesas)
        this.despesas = resultado.despesas
        this.totalPaginas = resultado.totalPaginas
      } catch (error) {
        console.error("Erro ao carregar despesas:", error)
        this.baseStore.showSnackbar("Erro ao carregar as despesas.")
      }
    },
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
        justificativa: this.justificativa,
        user_id: this.accountsStore.loggedUser?.id,
      }

      try {
        let resultado;
        
        if (this.modoEdicao && this.despesaEmEdicao) {
          // Modo de edição
          payload.id = this.despesaEmEdicao.id;
          resultado = await this.coreStore.updateDespesa(payload);
          this.baseStore.showSnackbar("Despesa atualizada com sucesso!");
        } else {
          // Modo de adição
          resultado = await this.coreStore.addDespesa(payload);
          this.baseStore.showSnackbar("Gasto lançado com sucesso!");
        }

        // Resetar formulário
        this.resetarFormulario();

        // Recarregar lista de despesas
        this.carregarDespesas(this.despesasPage);
      } catch (error) {
        console.error("Erro ao lançar/atualizar gasto:", error);
        this.baseStore.showSnackbar("Erro ao lançar/atualizar o gasto. Tente novamente.");
      }
    },
    resetarFormulario() {
      this.valor = null;
      this.valorFormatado = '';
      this.elementoSelecionado = null;
      this.tipoGastosDisponiveis = [];
      this.tipoGastoSelecionado = null;
      this.justificativa = '';
      this.modoEdicao = false;
      this.despesaEmEdicao = null;
    },
    cancelarEdicao() {
      this.resetarFormulario();
    },
    podeDeletarDespesa(despesa) {
      // Verifica se a despesa é do usuário logado
      if (despesa.usuario.id !== this.accountsStore.loggedUser?.id) {
        return false;
      }

      // Converte a data de criação para objeto Date
      const dataCriacao = new Date(despesa.created_at);
      const agora = new Date();
      
      // Calcula a diferença em minutos
      const diferencaMinutos = (agora - dataCriacao) / (1000 * 60);
      
      // Retorna true se a despesa tiver menos de 5 minutos
      return diferencaMinutos < 5;
    },
    podeEditarDespesa(despesa) {
      // Verifica se a despesa é do usuário logado
      return despesa.usuario.id === this.accountsStore.loggedUser?.id;
    },
    formatarData(dataString) {
      // Converte a string de data para objeto Date
      const data = new Date(dataString);
      
      // Formata a data para o formato brasileiro
      return data.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      });
    },
    async deletarDespesa(despesaId) {
      try {
        await this.coreStore.deleteDespesa(despesaId);
        this.baseStore.showSnackbar("Despesa deletada com sucesso!");
        // Recarrega a lista de despesas
        this.carregarDespesas(this.despesasPage);
      } catch (error) {
        console.error("Erro ao deletar despesa:", error);
        this.baseStore.showSnackbar("Erro ao deletar a despesa. Tente novamente.");
      }
    },
    editarDespesa(despesa) {
      // Preenche o formulário com os dados da despesa
      this.valorFormatado = this.formatarValorExibicao(despesa.valor);
      this.elementoSelecionado = despesa.elemento.id;
      this.justificativa = despesa.justificativa;
      
      // Carrega os tipos de gasto para o elemento selecionado
      this.carregarTiposGasto().then(() => {
        this.tipoGastoSelecionado = despesa.tipoGasto.id;
      });
      
      // Marca o modo de edição
      this.modoEdicao = true;
      this.despesaEmEdicao = despesa;
      
      // Rola a página para o formulário
      this.$nextTick(() => {
        const formElement = document.querySelector('.v-form');
        if (formElement) {
          formElement.scrollIntoView({ behavior: 'smooth' });
        }
      });
    },
  },
}
</script>

<style scoped></style>
