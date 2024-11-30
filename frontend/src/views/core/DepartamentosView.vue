<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card>
          <!-- Título e Botão na mesma linha -->
          <v-row no-gutters align="center">
            <v-col>
              <v-card-title class="headline" align="center">
                Departamentos
              </v-card-title>
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
    }
  },
  computed: {
    ...mapState(useCoreStore, ["departamentos", "departamentosLoading"]),
  },
  mounted() {
    this.getDepartamentos()
  },
  methods: {
    getDepartamentos() {
     // Simula uma chamada à API e insere detalhes fake
      this.coreStore.getDepartamentos().then(() => {
        this.coreStore.departamentos = this.coreStore.departamentos.map(departamento => ({
          ...departamento,
          gastos: [
            { id: 1, descricao: "Compra de materiais", valor: 10542.00 },
            { id: 2, descricao: "Manutenção de equipamentos", valor: 8540.00 },
            { id: 3, descricao: "Treinamento", valor: 8360.00 },
          ],
        }));
      });
    },
    toggleDepartment(departmentId) {
      this.activeDepartmentId =
        this.activeDepartmentId === departmentId ? null : departmentId;
    },
  },
}
</script>
