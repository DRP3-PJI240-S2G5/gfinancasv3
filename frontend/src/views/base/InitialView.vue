<template>
  <v-container class="mt-10">
    <v-row justify="center">
      <v-col cols="4">
        <card-option cardOptionTitle="Administração" cardOptionDescription="Administração geral do sistema" cardOptionLink="/gestao" cardOptionIcon="mdi-cog">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Gestão Departamentos" cardOptionDescription="Gestão dos Departamentos" cardOptionLink="/inicial" cardOptionIcon="mdi-store-cog">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Gastos e despesas" cardOptionDescription="Lançamentos de gastos e/ou despesas" cardOptionLink="/gastos" cardOptionIcon="mdi-currency-usd">
        </card-option>
      </v-col>

      <!-- Vou deixar esse laço for aqui para refatorar. Colocar todos os botões em um laço for
      <v-col v-for=" item in departamentos" :key="item.id" cols="12">

      </v-col>
      -->
    </v-row>
    <v-row justify="center">
      <v-col cols="4">
        <card-option cardOptionTitle="Consultas" cardOptionDescription="Normas e Leis correlatas" cardOptionLink="/inicial" cardOptionIcon="mdi-text-box-search-outline">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Relatórios" cardOptionDescription="Relatórios gerais do sistema" cardOptionLink="/inicial" cardOptionIcon="mdi-finance">
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
import CardOption from "@/components/CardOption.vue"

export default {
  components: {
    CardOption
  }
}
</script>

<style scoped></style>
