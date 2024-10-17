<template>
  <v-container class="mt-10">
    <v-row justify="center"><v-card-title class="text-h6 text-md-h5 text-lg-h4">Gestão dos Departamentos</v-card-title></v-row>
    <v-row justify="center">
      <v-col cols="4">
        <card-option cardOptionTitle="Criar novo" cardOptionDescription="Cadastro de novos departamentos" cardOptionLink="/gdepartamentos/criar" cardOptionIcon="mdi-store-plus">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Adicionar Colaboradores" cardOptionDescription="Atribuição de usuários" cardOptionLink="/gdepartamentos/addcolaborador" cardOptionIcon="mdi-badge-account-horizontal">
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
