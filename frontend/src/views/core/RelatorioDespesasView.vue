<template>
    <v-container class="mt-10">
        <v-row justify="center">
            <v-col cols="12">
                <v-card>
                    <v-card-title class="headline">
                        Relatório de Despesas por Departamento
                    </v-card-title>

                    <v-card-text>
                        <v-data-table :headers="headers" :items="despesasPorDepartamento" :loading="loading"
                            class="elevation-1">
                            <template v-slot:item.total_despesas="{ item }">
                                {{ formatarValor(item.total_despesas) }}
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useCoreStore } from '@/stores/coreStore'

export default {
    name: 'RelatorioDespesasView',
    setup() {
        const coreStore = useCoreStore()
        const loading = ref(false)
        const despesasPorDepartamento = ref([])

        const headers = [
            { title: 'Departamento', key: 'departamento_nome' },
            { title: 'Total de Despesas', key: 'total_despesas', align: 'end' }
        ]

        function formatarValor(valor) {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(valor)
        }

        async function carregarDados() {
            loading.value = true
            try {
                // Primeiro carrega os departamentos
                await coreStore.getDepartamentos()

                // Para cada departamento, carrega o total de despesas
                const dados = await Promise.all(
                    coreStore.departamentos.map(async (departamento) => {
                        const resultado = await coreStore.getTotalDespesasDepartamento(departamento.id)
                        return {
                            departamento_nome: departamento.nome,
                            total_despesas: resultado.total_despesas || 0
                        }
                    })
                )

                despesasPorDepartamento.value = dados
            } catch (error) {
                console.error('Erro ao carregar dados:', error)
            } finally {
                loading.value = false
            }
        }

        onMounted(() => {
            carregarDados()
        })

        return {
            loading,
            despesasPorDepartamento,
            headers,
            formatarValor
        }
    }
}
</script>

<style scoped></style>