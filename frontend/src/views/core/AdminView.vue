<template>
  <v-container class="mt-10">
    <v-row justify="center">
      <v-col cols="4">
        <card-option cardOptionTitle="Usuários" cardOptionDescription="Cadastro de novos usuários">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Departamentos/Entidades" cardOptionDescription="Cadastro de novos departamentos/entidades">
        </card-option>
      </v-col>

      <v-col cols="4">
        <card-option cardOptionTitle="Permissionamentos" cardOptionDescription="Atribuição de acessos e permissões">
        </card-option>
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
