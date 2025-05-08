<template>
    <v-container class="mt-10">
        <v-row justify="center">
            <v-col cols="12" md="6">
                <v-card>
                    <v-card-title class="headline">
                        Relatório de Despesas por Departamento
                    </v-card-title>

                    <v-card-text style="height: 400px;">
                        <canvas ref="chartCanvas"></canvas>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12" md="6">
                <v-card>
                    <v-card-title class="headline">
                        Tabela de Despesas
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
import { ref, onMounted, computed, watch } from 'vue'
import { useCoreStore } from '@/stores/coreStore'

export default {
    name: 'RelatorioDespesasView',
    setup() {
        const coreStore = useCoreStore()
        const loading = ref(false)
        const despesasPorDepartamento = ref([])
        const chartCanvas = ref(null)
        let chart = null

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

        function carregarChartJS() {
            return new Promise((resolve) => {
                if (window.Chart) {
                    resolve(window.Chart)
                } else {
                    const script = document.createElement('script')
                    script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
                    script.onload = () => resolve(window.Chart)
                    document.head.appendChild(script)
                }
            })
        }

        async function criarGrafico() {
            if (chart) {
                chart.destroy()
            }

            const Chart = await carregarChartJS()
            const ctx = chartCanvas.value.getContext('2d')
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: despesasPorDepartamento.value.map(item => item.departamento_nome),
                    datasets: [{
                        label: 'Total de Despesas',
                        data: despesasPorDepartamento.value.map(item => item.total_despesas),
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Despesas por Departamento'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return new Intl.NumberFormat('pt-BR', {
                                        style: 'currency',
                                        currency: 'BRL'
                                    }).format(value)
                                }
                            }
                        }
                    }
                }
            })
        }

        async function carregarDados() {
            loading.value = true
            try {
                await coreStore.getDepartamentos()

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

        watch(despesasPorDepartamento, () => {
            if (chartCanvas.value) {
                criarGrafico()
            }
        }, { deep: true })

        onMounted(() => {
            carregarDados()
        })

        return {
            loading,
            despesasPorDepartamento,
            headers,
            formatarValor,
            chartCanvas
        }
    }
}
</script>

<style scoped>
.v-card {
    height: 100%;
}
</style>