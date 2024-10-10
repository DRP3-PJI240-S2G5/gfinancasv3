<template>
  <v-container class="mt-10">
    <v-row justify="center">
      <v-col cols="4">
        <card-option cardOptionTitle="Administração" cardOptionDescription="Administração geral do sistema" cardOptionLink="/inicial/administracao">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Gestão Departamentos" cardOptionDescription="Gestão dos Departamentos" cardOptionLink="/administracao">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Gastos e despesas" cardOptionDescription="Lançamentos de gastos e/ou despesas" cardOptionLink="/administracao">
        </card-option>
      </v-col>

      <!-- Vou deixar esse laço for aqui para refatorar. Colocar todos os botões em um laço for
      <v-col v-for=" item in departamentos" :key="item.id" cols="12">

      </v-col>
      -->
    </v-row>
    <v-row justify="center">
      <v-col cols="4">
        <card-option cardOptionTitle="Consultas" cardOptionDescription="Normas e Leis correlatas" cardOptionLink="/administracao">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Relatórios" cardOptionDescription="Relatórios gerais do sistema" cardOptionLink="/administracao">
        </card-option>
      </v-col>

      <v-col cols="4">

      </v-col>

      <!-- Vou deixar esse laço for aqui para refatorar. Colocar todos os botões em um laço for
      <v-col v-for=" item in departamentos" :key="item.id" cols="12">

      </v-col>
      -->
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { usecoreStore } from "@/stores/coreStore"
import CardOption from "@/components/CardOption.vue"

export default {
  components: {
    CardOption
  }
}
</script>

<style scoped></style>
