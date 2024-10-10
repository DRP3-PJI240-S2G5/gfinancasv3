<template>
  <v-footer :absolute="!fixed" color="#D40000" app>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" lg="6" md="6" align-self="center" class="pa-0">
          <div class="px-5 text-center">
            <span v-if="user" class="pl-4">
              <v-icon>mdi-account</v-icon>
              {{ user.username }}
            </span>
            <span class="px-5">ENV: {{ nodeEnv }}</span>
          </div>
        </v-col>
        <v-col cols="12" lg="6" md="6" align-self="center" class="pa-0">
          <div class="px-5 text-center">
            <span class="px-5">Você está em: {{ currentPath }}</span> <!-- Aqui exibimos o path atual -->
          </div>
        </v-col>
        <v-col cols="12" align-self="center" class="pa-0 text-center">
          <span> &copy; {{ new Date().getFullYear() }} - GFinanças                                                                                                                                                                                                                                          </span>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
export default {
  props: {
    fixed: {
      type: Boolean,
      default: true,
    },
    user: {
      type: Object,
      default: null,
    },
  },
  data() {
    return{
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
      nodeEnv: import.meta.env.VITE_NODE_ENV,
      currentPath: this.$route.path, // Obtém o caminho atual da URL
    };
  },
  watch: {
    // Observa mudanças na rota para atualizar o caminho atual
    $route(to) {
      this.currentPath = to.path;
    },
  },
}
</script>
