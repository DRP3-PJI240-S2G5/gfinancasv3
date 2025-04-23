<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <!-- Título e Botão na mesma linha -->
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline">
                Subordinações
              </v-card-title>
            </v-col>
            <v-col class="d-flex justify-end">
              <v-btn @click="criarNovaSubordinacao" color="primary" fab small>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="subordinacoes"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.departamento_superior="{ item }">
                {{ item.superior?.nome || 'N/A' }}
              </template>
              <template v-slot:item.departamento_subordinado="{ item }">
                {{ item.subordinado?.nome || 'N/A' }}
              </template>
              <template v-slot:item.acoes="{ item }">
                <v-btn
                  icon
                  variant="text"
                  color="primary"
                  size="small"
                  @click="editarSubordinacao(item)"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  color="error"
                  size="small"
                  @click="excluirSubordinacao(item)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog para criar/editar subordinação -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="editedItem.departamento_superior_id"
                  :items="departamentosSuperioresDisponiveis"
                  item-title="nome"
                  item-value="id"
                  label="Departamento Superior"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="editedItem.departamento_subordinado_id"
                  :items="departamentosDisponiveis"
                  item-title="nome"
                  item-value="id"
                  label="Departamento Subordinado"
                  required
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="text" @click="fecharDialog">
            Cancelar
          </v-btn>
          <v-btn color="primary" variant="text" @click="salvar">
            Salvar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog de confirmação para exclusão -->
    <v-dialog v-model="dialogDelete" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirmar exclusão</v-card-title>
        <v-card-text>
          Tem certeza que deseja excluir esta subordinação?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="text" @click="fecharDialogDelete">
            Cancelar
          </v-btn>
          <v-btn color="primary" variant="text" @click="confirmarExclusao">
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar para mensagens de erro -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn
          color="white"
          variant="text"
          @click="snackbar.show = false"
        >
          Fechar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useCoreStore } from '@/stores/coreStore'

const coreStore = useCoreStore()
const loading = ref(false)
const dialog = ref(false)
const dialogDelete = ref(false)
const subordinacoes = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  id: null,
  departamento_superior_id: null,
  departamento_subordinado_id: null
})
const defaultItem = ref({
  id: null,
  departamento_superior_id: null,
  departamento_subordinado_id: null
})

// Configuração do snackbar
const snackbar = ref({
  show: false,
  text: '',
  color: 'error',
  timeout: 5000
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Departamento Superior', key: 'departamento_superior' },
  { title: 'Departamento Subordinado', key: 'departamento_subordinado' },
  { title: 'Ações', key: 'acoes', sortable: false }
]

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Nova Subordinação' : 'Editar Subordinação'
})

const departamentosDisponiveis = computed(() => {
  if (!editedItem.value.departamento_superior_id) {
    return coreStore.departamentos
  }
  return coreStore.departamentos.filter(d => d.id !== editedItem.value.departamento_superior_id)
})

const departamentosSuperioresDisponiveis = computed(() => {
  if (!editedItem.value.departamento_subordinado_id) {
    return coreStore.departamentos
  }
  return coreStore.departamentos.filter(d => d.id !== editedItem.value.departamento_subordinado_id)
})

onMounted(async () => {
  await Promise.all([
    carregarSubordinacoes(),
    coreStore.getDepartamentos()
  ])
})

async function carregarSubordinacoes() {
  loading.value = true
  try {
    await coreStore.getSubordinacoes()
    subordinacoes.value = coreStore.subordinacoes
  } catch (error) {
    console.error('Erro ao carregar subordinações:', error)
  } finally {
    loading.value = false
  }
}

function criarNovaSubordinacao() {
  editedItem.value = Object.assign({}, defaultItem.value)
  editedIndex.value = -1
  dialog.value = true
}

function editarSubordinacao(item) {
  editedIndex.value = subordinacoes.value.indexOf(item)
  editedItem.value = {
    id: item.id,
    departamento_superior_id: item.superior.id,
    departamento_subordinado_id: item.subordinado.id
  }
  dialog.value = true
}

async function excluirSubordinacao(item) {
  if (!item || !item.id) {
    console.error('ID da subordinação inválido')
    return
  }
  
  editedIndex.value = subordinacoes.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialogDelete.value = true
}

async function confirmarExclusao() {
  try {
    await coreStore.deleteSubordinacao(editedItem.value.id)
    subordinacoes.value.splice(editedIndex.value, 1)
    fecharDialogDelete()
    snackbar.value = {
      show: true,
      text: 'Subordinação excluída com sucesso!',
      color: 'success',
      timeout: 3000
    }
  } catch (error) {
    console.error('Erro ao excluir subordinação:', error)
    snackbar.value = {
      show: true,
      text: 'Erro ao excluir subordinação. Por favor, tente novamente.',
      color: 'error',
      timeout: 5000
    }
  }
}

function fecharDialog() {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem.value)
  editedIndex.value = -1
}

function fecharDialogDelete() {
  dialogDelete.value = false
  editedItem.value = Object.assign({}, defaultItem.value)
  editedIndex.value = -1
}

async function salvar() {
  try {
    if (editedItem.value.departamento_superior_id === editedItem.value.departamento_subordinado_id) {
      snackbar.value = {
        show: true,
        text: 'O departamento superior e subordinado não podem ser o mesmo.',
        color: 'error',
        timeout: 5000
      }
      return
    }

    const payload = {
      IdDepartamentoA: editedItem.value.departamento_superior_id,
      IdDepartamentoB: editedItem.value.departamento_subordinado_id
    }

    if (editedIndex.value > -1) {
      payload.id = editedItem.value.id
      await coreStore.updateSubordinacao(payload)
      await carregarSubordinacoes()
      snackbar.value = {
        show: true,
        text: 'Subordinação atualizada com sucesso!',
        color: 'success',
        timeout: 3000
      }
    } else {
      await coreStore.createSubordinacao(payload)
      await carregarSubordinacoes()
      snackbar.value = {
        show: true,
        text: 'Subordinação criada com sucesso!',
        color: 'success',
        timeout: 3000
      }
    }
    fecharDialog()
  } catch (error) {
    console.error('Erro ao salvar subordinação:', error)
    let mensagem = 'Erro ao salvar subordinação. Por favor, tente novamente.'
    
    if (error.response?.data?.error) {
      const erro = error.response.data.error
      if (erro.includes('já possui uma subordinação direta')) {
        mensagem = 'Este departamento já possui uma subordinação direta com outro departamento.'
      } else if (erro.includes('criaria um ciclo na hierarquia')) {
        mensagem = 'Não é possível criar esta subordinação pois ela criaria um ciclo na hierarquia.'
      } else if (erro.includes('subordinação já existe')) {
        mensagem = 'Esta relação de subordinação já existe.'
      }
    }
    
    snackbar.value = {
      show: true,
      text: mensagem,
      color: 'error',
      timeout: 5000
    }
  }
}
</script> 