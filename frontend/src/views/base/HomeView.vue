<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-card-title class="text-h6 text-md-h5 text-lg-h4">Secretaria Municipal de Esportes e Lazer</v-card-title>
      <div class="py-6" />
      <div class="d-flex justify-center align-center">
        <v-img class="mx-2" contain height="200" src="@/assets/bandeira-pinda-v2.svg" />
        <v-img class="mx-2" contain height="200" src="@/assets/cropped-semelp.png" />
        <v-img class="mx-2" contain height="200" src="@/assets/brasao-pinda.png" />
      </div>
      <div class="text-body-1 mt-n1 pt-4">Gerenciameno Financeiro - SEMELP</div>
      <h1 class="text-h4 font-weight-bold">Sistema G Finanças</h1>

      <div class="py-6" />

      <v-row class="d-flex align-center justify-center">
        <v-col cols="auto">
          <v-btn
            color="primary"
            href="https://semelp.pindamonhangaba.sp.gov.br/"
            target="_blank"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            variant="flat"
            class="my-4 mr-2">
            <v-icon icon="mdi-exit-to-app" size="large" start />
            portal SEMELP
          </v-btn>
          <v-btn
            v-if="!loggedUser"
            color="primary"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            variant="flat"
            :to="{ name: 'accounts-login' }"
            class="my-4 mr-2">
            <v-icon icon="mdi-account-arrow-right-outline" size="large" start />
            Entrar
          </v-btn>
          <v-btn
            v-else
            color="primary"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            variant="flat"
            :to="{ name: 'accounts-logout' }">
            <v-icon icon="mdi-account-arrow-right-outline" size="large" start />
            Sair
          </v-btn>
          <v-btn
            v-if="loggedUser"
            color="primary"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            variant="flat"
            :to="{ name: 'departamentos-list' }"
            class="my-4 mr-2">
            <v-icon icon="mdi-folder-star-multiple" size="large" start />
            departamentos
          </v-btn>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useAccountsStore } from "@/stores/accountsStore"

export default {
  computed: {
    ...mapState(useAccountsStore, ["loggedUser"]),
  },
}
</script>
