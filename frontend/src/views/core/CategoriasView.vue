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
          <elemento-form 
            :form-label="formElementoLabel" 
            :elemento="elementoEditando"
            @new-elemento="addElemento"
            @update-elemento="updateElemento"
            @cancel="toggleFormElemento"
          />
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
            <template v-slot:append>
              <v-btn
                icon
                variant="text"
                color="primary"
                @click.stop="editElemento(item)"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn
                icon
                variant="text"
                color="error"
                @click.stop="deleteElemento(item)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
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
            @new-tipo-gasto="addTipoGasto" 
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
            <v-list-item-title>{{ item.tipoGasto.tipoGasto }}</v-list-item-title>
            <v-list-item-subtitle>{{ item.descricao }}</v-list-item-subtitle>
            <template v-slot:append>
              <v-btn
                icon
                variant="text"
                color="error"
                @click="deletarTipoGasto(item)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>

    <confirm-dialog
      v-model="showConfirmDialog"
      title="Excluir Elemento"
      :message="confirmMessage"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useCoreStore } from "@/stores/coreStore"
import TipoGastoForm from "@/components/TipoGastoForm.vue"
import ElementoForm from "@/components/ElementoForm.vue"
import ConfirmDialog from "@/components/ConfirmDialog.vue"

export default {
  name: "CategoriasView",
  components: { TipoGastoForm, ElementoForm, ConfirmDialog },
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
      tipoGastosDoElemento: [],
      showConfirmDialog: false,
      elementoToDelete: null,
      tipoGastoToDelete: null,
      confirmMessage: '',
      elementoEditando: null
    }
  },
  computed: {
    ...mapState(useCoreStore, ["elementos", "elementosLoading", "tipoGastos", "tipoGastosLoading"]),
    formElementoLabel() {
      return this.elementoEditando ? 'Editar Elemento' : 'Novo Elemento'
    }
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
    async addTipoGasto(tipoGasto) {
      try {
        const newTipoGasto = await this.coreStore.addTipoGasto(tipoGasto)
        this.baseStore.showSnackbar(`Novo tipo de gasto adicionado: ${newTipoGasto.tipoGasto}`)
        this.getTipoGastos()
        this.carregarTiposGastoDoElemento(this.elementoSelecionado.id)
        this.showFormTipoGasto = false
      } catch (error) {
        console.error("Erro ao adicionar tipo de gasto:", error)
        const mensagemErro = error.response?.data?.detail || error.message || "Erro ao adicionar tipo de gasto"
        this.baseStore.showSnackbar(mensagemErro, "error")
      }
    },
    toggleFormTipoGasto() {
      this.showFormTipoGasto = !this.showFormTipoGasto
    },
    getElementos() {
      this.coreStore.getElementos()
    },
    async addElemento(elemento) {
      try {
        const newElemento = await this.coreStore.addElemento(elemento)
        this.baseStore.showSnackbar(`Novo elemento adicionado: ${newElemento.elemento}`)
        this.getElementos()
        this.showFormElemento = false
      } catch (error) {
        console.error("Erro ao adicionar elemento:", error)
        const mensagemErro = error.response?.data?.detail || error.message || "Erro ao adicionar elemento"
        this.baseStore.showSnackbar(mensagemErro, "error")
      }
    },
    toggleFormElemento() {
      this.showFormElemento = !this.showFormElemento
      if (!this.showFormElemento) {
        this.elementoEditando = null
      }
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
    async deletarTipoGasto(tipoGasto) {
      this.tipoGastoToDelete = tipoGasto
      this.confirmMessage = `Tem certeza que deseja excluir o tipo de gasto "${tipoGasto.tipoGasto.tipoGasto}"?`
      this.showConfirmDialog = true
    },
    async confirmDelete() {
      try {
        if (this.elementoToDelete) {
          await this.coreStore.deleteElemento(this.elementoToDelete.id)
          this.baseStore.showSnackbar('Elemento excluído com sucesso')
          await this.getElementos()
          if (this.elementoSelecionado?.id === this.elementoToDelete.id) {
            this.elementoSelecionado = null
          }
        } else if (this.tipoGastoToDelete) {
          await this.coreStore.deleteTipoGasto(this.tipoGastoToDelete.tipoGasto.id)
          this.baseStore.showSnackbar('Tipo de gasto excluído com sucesso')
          await this.carregarTiposGastoDoElemento(this.elementoSelecionado.id)
        }
      } catch (error) {
        console.error('Erro ao excluir:', error)
        this.baseStore.showSnackbar('Erro ao excluir', 'error')
      } finally {
        this.elementoToDelete = null
        this.tipoGastoToDelete = null
        this.showConfirmDialog = false
      }
    },
    cancelDelete() {
      this.elementoToDelete = null
      this.tipoGastoToDelete = null
      this.showConfirmDialog = false
    },
    editElemento(elemento) {
      this.elementoEditando = { ...elemento }
      this.showFormElemento = true
    },
    async updateElemento(elemento) {
      try {
        const elementoAtualizado = await this.coreStore.updateElemento(elemento)
        this.baseStore.showSnackbar(`Elemento atualizado: ${elementoAtualizado.elemento}`)
        await this.getElementos()
        this.showFormElemento = false
        this.elementoEditando = null
      } catch (error) {
        console.error('Erro ao atualizar elemento:', error)
        this.baseStore.showSnackbar('Erro ao atualizar elemento', 'error')
      }
    },
    deleteElemento(elemento) {
      this.elementoToDelete = elemento
      this.confirmMessage = `Tem certeza que deseja excluir o elemento "${elemento.elemento}"?`
      this.showConfirmDialog = true
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
