<template>
    <v-container class="mt-10">
        <v-row>
            <v-col cols="12">
                <v-card>
                    <v-card-title class="headline">
                        Consulta de Legislações
                    </v-card-title>

                    <v-card-text>
                        <v-row>
                            <v-col cols="12" md="4">
                                <v-text-field
                                    v-model="searchTerm"
                                    label="Buscar legislação"
                                    prepend-icon="mdi-magnify"
                                    @input="filtrarLegislacoes"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12" md="4">
                                <v-select
                                    v-model="tipoFiltro"
                                    :items="tiposLegislacao"
                                    label="Tipo de Legislação"
                                    @update:model-value="filtrarLegislacoes"
                                ></v-select>
                            </v-col>
                        </v-row>

                        <v-data-table
                            :headers="headers"
                            :items="legislacoesFiltradas"
                            :loading="loading"
                            class="elevation-1"
                        >
                            <template v-slot:item.acoes="{ item }">
                                <v-btn
                                    color="primary"
                                    icon
                                    @click="visualizarLegislacao(item)"
                                >
                                    <v-icon>mdi-eye</v-icon>
                                </v-btn>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Dialog para visualizar a legislação -->
        <v-dialog v-model="dialog" max-width="800px">
            <v-card>
                <v-card-title>
                    {{ legislacaoSelecionada?.titulo }}
                </v-card-title>
                <v-card-text>
                    <div v-if="legislacaoSelecionada">
                        <p><strong>Tipo:</strong> {{ legislacaoSelecionada.tipo }}</p>
                        <p><strong>Número:</strong> {{ legislacaoSelecionada.numero }}</p>
                        <p><strong>Data de Publicação:</strong> {{ formatarData(legislacaoSelecionada.data_publicacao) }}</p>
                        <v-divider class="my-4"></v-divider>
                        <div class="text-body-1">
                            {{ legislacaoSelecionada.conteudo }}
                        </div>
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="dialog = false">Fechar</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useCoreStore } from '@/stores/coreStore'

export default {
    name: 'LegislacoesView',
    setup() {
        const coreStore = useCoreStore()
        const loading = ref(false)
        const searchTerm = ref('')
        const tipoFiltro = ref('')
        const dialog = ref(false)
        const legislacaoSelecionada = ref(null)

        const tiposLegislacao = [
            'Lei',
            'Decreto',
            'Portaria',
            'Instrução Normativa',
            'Resolução'
        ]

        const headers = [
            { title: 'Título', key: 'titulo' },
            { title: 'Tipo', key: 'tipo' },
            { title: 'Número', key: 'numero' },
            { title: 'Data de Publicação', key: 'data_publicacao' },
            { title: 'Ações', key: 'acoes', sortable: false }
        ]

        const legislacoesFiltradas = computed(() => {
            return coreStore.legislacoes
        })

        function formatarData(data) {
            return new Date(data).toLocaleDateString('pt-BR')
        }

        async function visualizarLegislacao(legislacao) {
            try {
                const legislacaoDetalhada = await coreStore.getLegislacao(legislacao.id)
                legislacaoSelecionada.value = legislacaoDetalhada
                dialog.value = true
            } catch (error) {
                console.error('Erro ao carregar legislação:', error)
            }
        }

        async function filtrarLegislacoes() {
            loading.value = true
            try {
                await coreStore.searchLegislacoes(searchTerm.value, tipoFiltro.value)
            } catch (error) {
                console.error('Erro ao filtrar legislações:', error)
            } finally {
                loading.value = false
            }
        }

        onMounted(async () => {
            loading.value = true
            try {
                await coreStore.getLegislacoes()
            } catch (error) {
                console.error('Erro ao carregar legislações:', error)
            } finally {
                loading.value = false
            }
        })

        return {
            loading,
            searchTerm,
            tipoFiltro,
            tiposLegislacao,
            headers,
            legislacoesFiltradas,
            dialog,
            legislacaoSelecionada,
            formatarData,
            visualizarLegislacao,
            filtrarLegislacoes
        }
    }
}
</script>

<style scoped>
.v-card {
    height: 100%;
}
</style> 