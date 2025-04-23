<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <!-- Título e Filtro de Ano na mesma linha -->
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline" align="center">
                Departamentos
              </v-card-title>
            </v-col>
            <v-col cols="auto" class="pr-4">
              <v-select
                v-model="anoSelecionado"
                :items="anosDisponiveis"
                label="Ano"
                density="compact"
                variant="outlined"
                hide-details
                class="mt-2"
                style="max-width: 120px;"
                @update:model-value="atualizarAno"
              ></v-select>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-col
        v-for="item in departamentos"
        :key="item.id"
        cols="12"
        v-show="!activeDepartmentId || activeDepartmentId === item.id"
      >
        <f-departamento
          :departamento="item"
          :is-active="activeDepartmentId === item.id"
          :ano-selecionado="anoSelecionado"
          @toggle-department="toggleDepartment"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useCoreStore } from "@/stores/coreStore"
import FDepartamento from "@/components/FDepartamento.vue"

export default {
  name: "DepartamentosView",
  components: { FDepartamento },
  setup() {
    const baseStore = useBaseStore()
    const coreStore = useCoreStore()
    return { baseStore, coreStore }
  },
  data() {
    return {
      activeDepartmentId: null, // Armazena o departamento expandido
      departamentoAtivo: null,
      dialog: false,
      anoSelecionado: new Date().getFullYear(),
      anosDisponiveis: [],
      editedItem: {
        id: null,
        nome: "",
        descricao: "",
        verba_total: 0
      },
      defaultItem: {
        id: null,
        nome: "",
        descricao: "",
        verba_total: 0
      }
    }
  },
  computed: {
    ...mapState(useCoreStore, ["departamentos", "departamentosLoading"]),
  },
  async mounted() {
    this.gerarAnosDisponiveis()
    await this.carregarDados()
  },
  methods: {
    gerarAnosDisponiveis() {
      const anoAtual = new Date().getFullYear()
      this.anosDisponiveis = []
      // Gera uma lista de anos de 5 anos atrás até 5 anos no futuro
      for (let i = anoAtual - 5; i <= anoAtual + 5; i++) {
        this.anosDisponiveis.push(i)
      }
    },
    atualizarAno() {
      // Este método será chamado quando o ano for alterado
      console.log("Ano selecionado:", this.anoSelecionado)
    },
    async carregarDados() {
      try {
        await this.coreStore.getDepartamentos()
        await this.coreStore.getSubordinacoes()
      } catch (error) {
        console.error("Erro ao carregar dados:", error)
      }
    },
    toggleDepartment(departmentId) {
      this.activeDepartmentId =
        this.activeDepartmentId === departmentId ? null : departmentId;
    },
    async salvar() {
      try {
        if (this.editedItem.id) {
          await this.coreStore.updateDepartamento(this.editedItem)
        } else {
          await this.coreStore.createDepartamento(this.editedItem)
        }
        this.dialog = false
        this.editedItem = Object.assign({}, this.defaultItem)
        await this.carregarDados()
      } catch (error) {
        console.error("Erro ao salvar departamento:", error)
      }
    },
    editarItem(item) {
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    fecharDialog() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
      })
    }
  },
}
</script>
