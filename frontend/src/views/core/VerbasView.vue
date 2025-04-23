<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <!-- Título e Botão na mesma linha -->
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline">
                Verbas
              </v-card-title>
            </v-col>
            <v-col class="d-flex justify-end">
              <v-btn @click="criarNovaVerba" color="primary" fab small>
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
              :items="verbas"
              :loading="loading"
              :items-per-page="itemsPerPage"
              :page="currentPage"
              :items-length="totalItems"
              @update:page="handlePageChange"
              @update:items-per-page="handleItemsPerPageChange"
              class="elevation-1"
            >
              <template v-slot:item.valor="{ item }">
                {{ formatarValorExibicao(item.valor) }}
              </template>
              <template v-slot:item.departamento="{ item }">
                {{ item.departamento?.nome || 'N/A' }}
              </template>
              <template v-slot:item.acoes="{ item }">
                <v-btn
                  icon
                  variant="text"
                  color="primary"
                  size="small"
                  @click="editarVerba(item)"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  color="error"
                  size="small"
                  @click="excluirVerba(item)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog para criar/editar verba -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="valorFormatado"
                  label="Valor"
                  type="text"
                  prefix="R$"
                  required
                  @input="validarEntradaValor"
                  @blur="formatarValor"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editedItem.ano"
                  label="Ano"
                  type="number"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedItem.departamento_id"
                  :items="departamentos"
                  item-title="nome"
                  item-value="id"
                  label="Departamento"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.descricao"
                  label="Descrição"
                  rows="3"
                ></v-textarea>
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
          Tem certeza que deseja excluir esta verba?
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

    <!-- Snackbar para mensagens -->
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
const verbas = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  id: null,
  valor: 0,
  ano: new Date().getFullYear(),
  departamento_id: null,
  descricao: ''
})
const defaultItem = ref({
  id: null,
  valor: 0,
  ano: new Date().getFullYear(),
  departamento_id: null,
  descricao: ''
})
const valorFormatado = ref('')

// Configuração da paginação
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalItems = ref(0)
const totalPages = ref(1)

// Configuração do snackbar
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 5000
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Valor', key: 'valor' },
  { title: 'Ano', key: 'ano' },
  { title: 'Departamento', key: 'departamento' },
  { title: 'Descrição', key: 'descricao' },
  { title: 'Ações', key: 'acoes', sortable: false }
]

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Nova Verba' : 'Editar Verba'
})

const departamentos = computed(() => {
  return coreStore.departamentos
})

onMounted(async () => {
  await Promise.all([
    carregarVerbas(),
    coreStore.getDepartamentos()
  ])
})

async function carregarVerbas() {
  loading.value = true
  try {
    await coreStore.getVerbas(currentPage.value, itemsPerPage.value)
    verbas.value = coreStore.verbas
    
    // Atualizar informações de paginação
    if (coreStore.verbasPaginacao) {
      totalItems.value = coreStore.verbasPaginacao.total
      totalPages.value = coreStore.verbasPaginacao.total_paginas
    }
  } catch (error) {
    console.error('Erro ao carregar verbas:', error)
    mostrarMensagem('Erro ao carregar verbas', 'error')
  } finally {
    loading.value = false
  }
}

function formatarValorExibicao(valor) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor)
}

function validarEntradaValor(event) {
  const valor = event.target.value;
  // Remove todos os caracteres que não são números, ponto ou vírgula
  const valorLimpo = valor.replace(/[^\d.,]/g, '');
  
  // Se houver alteração, atualiza após 300ms
  if (valorLimpo !== valor) {
    setTimeout(() => {
      valorFormatado.value = valorLimpo;
    }, 300);
  }

  // Remove os pontos após 300ms
  setTimeout(() => {
    if (valorFormatado.value.includes('.')) {
      valorFormatado.value = valorFormatado.value.replace(/\./g, '');
    }
  }, 300);
}

function formatarValor() {
  // Converte string com vírgula para número com ponto
  const numerico = parseFloat(valorFormatado.value.replace(',', '.'))
  if (!isNaN(numerico)) {
    editedItem.value.valor = numerico
  } else {
    editedItem.value.valor = 0
  }
}

function criarNovaVerba() {
  editedItem.value = Object.assign({}, defaultItem.value)
  valorFormatado.value = ''
  editedIndex.value = -1
  dialog.value = true
}

function editarVerba(item) {
  editedIndex.value = verbas.value.indexOf(item)
  editedItem.value = {
    id: item.id,
    valor: item.valor,
    ano: item.ano,
    departamento_id: item.departamento?.id || null,
    descricao: item.descricao || ''
  }
  valorFormatado.value = item.valor.toString().replace('.', ',')
  dialog.value = true
}

async function excluirVerba(item) {
  if (!item || !item.id) {
    console.error('ID da verba inválido')
    return
  }
  
  editedIndex.value = verbas.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialogDelete.value = true
}

async function confirmarExclusao() {
  try {
    await coreStore.deleteVerba(editedItem.value.id)
    verbas.value.splice(editedIndex.value, 1)
    mostrarMensagem('Verba excluída com sucesso')
    fecharDialogDelete()
  } catch (error) {
    console.error('Erro ao excluir verba:', error)
    mostrarMensagem('Erro ao excluir verba', 'error')
  }
}

function fecharDialogDelete() {
  dialogDelete.value = false
  editedItem.value = Object.assign({}, defaultItem.value)
}

function fecharDialog() {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem.value)
  valorFormatado.value = ''
}

async function salvar() {
  try {
    formatarValor() // Garante que o valor está formatado corretamente antes de salvar
    
    if (editedItem.value.id) {
      await coreStore.updateVerba(editedItem.value)
      Object.assign(verbas.value[editedIndex.value], editedItem.value)
      mostrarMensagem('Verba atualizada com sucesso')
    } else {
      const { id, ...novaVerba } = editedItem.value
      const verbaCriada = await coreStore.addVerba(novaVerba)
      verbas.value.push(verbaCriada)
      mostrarMensagem('Verba criada com sucesso')
    }
    fecharDialog()
  } catch (error) {
    console.error('Erro ao salvar verba:', error)
    mostrarMensagem('Erro ao salvar verba', 'error')
  }
}

function handlePageChange(page) {
  currentPage.value = page
  carregarVerbas()
}

function handleItemsPerPageChange(itemsPerPage) {
  itemsPerPage.value = itemsPerPage
  currentPage.value = 1 // Voltar para a primeira página ao mudar o número de itens
  carregarVerbas()
}

function mostrarMensagem(texto, cor = 'success') {
  snackbar.value = {
    show: true,
    text: texto,
    color: cor,
    timeout: 5000
  }
}
</script>
