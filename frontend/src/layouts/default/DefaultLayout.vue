<template>
  <VLayout>
    <app-error-dialog :show="showErrorMessage" :message="errorMessage" @close="closeErrorDialog" />
    <app-snackbar />
    <VApp :theme="theme">
      <app-nav-bar :theme="theme" @theme-click="onThemeClick"></app-nav-bar>
      <VMain :style="{ backgroundColor: theme === 'light' ? '#FFD' : '' }">
        <RouterView />
      </VMain>
      <app-footer :fixed="true" :user="loggedUser" />
    </VApp>
  </VLayout>
</template>

<script setup>
import { ref } from "vue"

const theme = ref("light")

function onThemeClick() {
  theme.value = theme.value === "light" ? "dark" : "light"
}
</script>

<script>
import { mapState } from "pinia"
import { useBaseStore } from "@/stores/baseStore"
import { useAccountsStore } from "@/stores/accountsStore"
import AppSnackbar from "@/components/AppSnackbar.vue"
import AppErrorDialog from "@/components/AppErrorDialog.vue"
import AppNavBar from "@/components/AppNavBar.vue"
import AppFooter from "@/components/AppFooter.vue"

export default {
  name: "DepartamentosLayout",
  components: {
    AppSnackbar,
    AppErrorDialog,
    AppNavBar,
    AppFooter,
  },
  setup() {
    const baseStore = useBaseStore()
    return { baseStore }
  },
  computed: {
    ...mapState(useBaseStore, ["errorMessage", "showErrorMessage"]),
    ...mapState(useAccountsStore, ["loggedUser"]),
  },
  methods: {
    closeErrorDialog() {
      this.baseStore.setShowErrorMessage(null)
    },
  },
}
</script>
