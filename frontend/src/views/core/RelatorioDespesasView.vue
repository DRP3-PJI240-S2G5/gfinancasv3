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
        const elementosDespesa = ref([])
        const chartCanvas = ref(null)
        let chart = null

        const headers = [
            { title: 'Departamento', key: 'departamento_nome' },
            { title: 'Total de Despesas', key: 'total_despesas', align: 'end' }
        ]

        const cores = [
            'rgba(220, 53, 69, 0.8)',    // Vermelho mais escuro
            'rgba(0, 123, 255, 0.8)',    // Azul mais escuro
            'rgba(255, 193, 7, 0.8)',    // Amarelo mais escuro
            'rgba(23, 162, 184, 0.8)',   // Ciano mais escuro
            'rgba(111, 66, 193, 0.8)',   // Roxo mais escuro
            'rgba(253, 126, 20, 0.8)',   // Laranja mais escuro
            'rgba(108, 117, 125, 0.8)',  // Cinza mais escuro
            'rgba(40, 84, 255, 0.8)',    // Azul royal mais escuro
            'rgba(40, 167, 69, 0.8)',    // Verde mais escuro
            'rgba(73, 80, 87, 0.8)'      // Cinza escuro
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

            console.log('Criando gráfico com dados:', {
                elementos: elementosDespesa.value,
                despesas: despesasPorDepartamento.value
            })

            const datasets = elementosDespesa.value.map((elemento, index) => {
                const data = despesasPorDepartamento.value.map(departamento => {
                    const elementoData = departamento.elementos.find(e => e.elemento_id === elemento.id)
                    return elementoData ? elementoData.valor : 0
                })
                
                console.log(`Dataset para elemento ${elemento.elemento}:`, data)
                
                return {
                    label: elemento.elemento,
                    data: data,
                    backgroundColor: cores[index % cores.length],
                    borderColor: cores[index % cores.length].replace('0.8', '1'),
                    borderWidth: 1
                }
            })

            const chartData = {
                labels: despesasPorDepartamento.value.map(item => item.departamento_nome),
                datasets: datasets
            }

            console.log('Dados do gráfico:', chartData)

            chart = new Chart(ctx, {
                type: 'bar',
                data: chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Despesas por Departamento e Elemento'
                        }
                    },
                    scales: {
                        x: {
                            stacked: true,
                        },
                        y: {
                            stacked: true,
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
                await coreStore.getElementos()
                elementosDespesa.value = coreStore.elementos
                
                console.log('Elementos carregados:', elementosDespesa.value)

                const dados = await Promise.all(
                    coreStore.departamentos.map(async (departamento) => {
                        const resultado = await coreStore.getTotalDespesasDepartamento(departamento.id)
                        const elementosData = await Promise.all(
                            elementosDespesa.value.map(async (elemento) => {
                                try {
                                    const valor = await coreStore.getTotalDespesasPorElemento(departamento.id, elemento.id)
                                    return {
                                        elemento_id: elemento.id,
                                        elemento_nome: elemento.elemento,
                                        valor: valor.total_despesas || 0
                                    }
                                } catch (error) {
                                    console.error(`Erro ao buscar despesas do elemento ${elemento.elemento}:`, error)
                                    return {
                                        elemento_id: elemento.id,
                                        elemento_nome: elemento.elemento,
                                        valor: 0
                                    }
                                }
                            })
                        )
                        
                        console.log(`Dados do departamento ${departamento.nome}:`, elementosData)
                        
                        return {
                            departamento_nome: departamento.nome,
                            total_despesas: resultado.total_despesas || 0,
                            elementos: elementosData
                        }
                    })
                )

                despesasPorDepartamento.value = dados
                console.log('Dados finais:', despesasPorDepartamento.value)
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