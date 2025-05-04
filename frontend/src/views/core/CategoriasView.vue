<template>
  <v-container class="fill-height">
    <v-row>
      <!-- COLUNA 1 - LISTA DE ELEMENTOS -->
      <v-col cols="12" md="4">
        <v-card class="mb-4">
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline">Elementos</v-card-title>
            </v-col>
            <v-col class="d-flex justify-end">
              <v-btn @click="toggleFormElemento" color="primary" fab small>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>

        <div v-if="showFormElemento" class="mb-4">
          <elemento-form :form-label="'Novo Elemento'" @new-elemento="addNewElemento" />
        </div>

        <v-list>
          <v-list-item
            v-for="item in elementos"
            :key="item.id"
            :class="{ 'bg-primary': elementoSelecionado?.id === item.id }"
            @click="selecionarElemento(item)"
          >
            <v-list-item-title>{{ item.elemento }}</v-list-item-title>
            <v-list-item-subtitle>{{ item.descricao }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-col>

      <!-- COLUNA 2 - TIPOS DE GASTOS DO ELEMENTO SELECIONADO -->
      <v-col cols="12" md="8">
        <v-card class="mb-4">
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline">
                Tipos de Gastos
                <span v-if="elementoSelecionado" class="text-caption ml-2">
                  ({{ elementoSelecionado.elemento }})
                </span>
              </v-card-title>
            </v-col>
            <v-col class="d-flex justify-end">
              <v-btn 
                v-if="elementoSelecionado"
                @click="toggleFormTipoGasto" 
                color="primary" 
                fab small
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>

        <div v-if="showFormTipoGasto" class="mb-4">
          <tipo-gasto-form 
            :form-label="'Novo Tipo de Gasto'" 
            :elemento-id="elementoSelecionado?.id"
            @new-tipo-gasto="addNewTipoGasto" 
          />
        </div>

        <v-alert
          v-if="!elementoSelecionado"
          type="info"
          class="mt-4"
        >
          Selecione um elemento para visualizar seus tipos de gastos
        </v-alert>

        <v-list v-else>
          <v-list-item
            v-for="item in tipoGastosDoElemento"
            :key="item.id"
          >
            <v-list-item-title>{{ item.tipoGasto }}</v-list-item-title>
            <v-list-item-subtitle>{{ item.descricao }}</v-list-item-subtitle>
            <template v-slot:append>
              <v-btn
                icon
                variant="text"
                color="error"
                @click="deletarTipoGasto(item.id)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useCoreStore } from "@/stores/coreStore"
import TipoGastoForm from "@/components/TipoGastoForm.vue"
import ElementoForm from "@/components/ElementoForm.vue"

export default {
  name: "CategoriasView",
  components: { TipoGastoForm, ElementoForm },
  setup() {
    const baseStore = useBaseStore()
    const coreStore = useCoreStore()
    return { baseStore, coreStore }
  },
  data() {
    return {
      showFormTipoGasto: false,
      showFormElemento: false,
      elementoSelecionado: null,
      tipoGastosDoElemento: []
    }
  },
  computed: {
    ...mapState(useCoreStore, ["elementos", "elementosLoading", "tipoGastos", "tipoGastosLoading"]),
  },
  watch: {
    elementoSelecionado: {
      handler(novoElemento) {
        if (novoElemento) {
          this.carregarTiposGastoDoElemento(novoElemento.id)
        } else {
          this.tipoGastosDoElemento = []
        }
      }
    }
  },
  mounted() {
    this.getTipoGastos()
    this.getElementos()
  },
  methods: {
    getTipoGastos() {
      this.coreStore.getTipoGastos()
    },
    async addNewTipoGasto(tipoGasto) {
      try {
        const newTipoGasto = await this.coreStore.addNewTipoGasto(tipoGasto)
        this.baseStore.showSnackbar(`Novo tipo de gasto adicionado: ${newTipoGasto.tipoGasto}`)
        this.getTipoGastos()
        this.carregarTiposGastoDoElemento(this.elementoSelecionado.id)
        this.showFormTipoGasto = false
      } catch (error) {
        console.error("Erro ao adicionar tipo de gasto:", error)
        this.baseStore.showSnackbar("Erro ao adicionar tipo de gasto", "error")
      }
    },
    toggleFormTipoGasto() {
      this.showFormTipoGasto = !this.showFormTipoGasto
    },
    getElementos() {
      this.coreStore.getElementos()
    },
    async addNewElemento(elemento) {
      try {
        const newElemento = await this.coreStore.addNewElemento(elemento)
        this.baseStore.showSnackbar(`Novo elemento adicionado: ${newElemento.elemento}`)
        this.getElementos()
        this.showFormElemento = false
      } catch (error) {
        console.error("Erro ao adicionar elemento:", error)
        this.baseStore.showSnackbar("Erro ao adicionar elemento", "error")
      }
    },
    toggleFormElemento() {
      this.showFormElemento = !this.showFormElemento
    },
    selecionarElemento(elemento) {
      this.elementoSelecionado = elemento
      this.showFormTipoGasto = false
    },
    async carregarTiposGastoDoElemento(elementoId) {
      try {
        const tiposGasto = await this.coreStore.getTipoGastosPorElemento(elementoId)
        this.tipoGastosDoElemento = tiposGasto
      } catch (error) {
        console.error("Erro ao carregar tipos de gasto:", error)
        this.baseStore.showSnackbar("Erro ao carregar tipos de gasto", "error")
      }
    },
    async deletarTipoGasto(tipoGastoId) {
      try {
        await this.coreStore.deleteTipoGasto(tipoGastoId)
        this.baseStore.showSnackbar("Tipo de gasto deletado com sucesso")
        this.carregarTiposGastoDoElemento(this.elementoSelecionado.id)
      } catch (error) {
        console.error("Erro ao deletar tipo de gasto:", error)
        this.baseStore.showSnackbar("Erro ao deletar tipo de gasto", "error")
      }
    }
  },
}
</script>

<style scoped>
.bg-primary {
  background-color: rgba(var(--v-theme-primary), 0.1);
}

.v-list {
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.v-list-item {
  margin-bottom: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.12);
  padding: 8px 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.v-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.1);
  border-color: rgba(var(--v-theme-primary), 0.5);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
</style>
