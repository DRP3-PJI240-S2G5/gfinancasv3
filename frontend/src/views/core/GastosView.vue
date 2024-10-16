<template>
  <v-container class="mt-10">
    <v-row justify="center"><v-card-title class="text-h6 text-md-h5 text-lg-h4">Gastos e Despesas</v-card-title></v-row>
    <v-row justify="center">
      <v-col cols="4">
        <card-option cardOptionTitle="Gabinete Secretário" cardOptionDescription="Lançar gastos ou despesas" cardOptionLink="/gastos/gabsecretario" cardOptionIcon="mdi-account-tie">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Departamentos de Esportes" cardOptionDescription="Lançar gastos ou despesas" cardOptionLink="/gastos/esportes" cardOptionIcon="mdi-soccer-field">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Departamentos de Lazer" cardOptionDescription="Lançar gastos ou despesas" cardOptionLink="/gastos/lazer" cardOptionIcon="mdi-beach">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Departamento Administrativo" cardOptionDescription="Lançar gastos ou despesas" cardOptionLink="/gastos/administrativo" cardOptionIcon="mdi-badge-account">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="F.A.E.P." cardOptionDescription="Lançar gastos ou despesas" cardOptionLink="/gastos/faep" cardOptionIcon="mdi-school">
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
