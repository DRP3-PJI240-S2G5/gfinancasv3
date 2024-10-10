<template>
  <v-app-bar color="#038C4C">
    <v-app-bar-title>{{ title }}</v-app-bar-title>
    <template #append>
      <!-- Botão de Voltar -->
      <v-btn v-if="!isHomePage" icon="mdi-arrow-left" @click="goBack"></v-btn>

      <v-btn icon="mdi-heart" :to="{ name: 'base-home' }"></v-btn>
      <v-btn icon="mdi-magnify"></v-btn>
      <v-btn
        :prepend-icon="theme === 'light' ? 'mdi-weather-sunny' : 'mdi-weather-night'"
        @click.stop="themeClick"></v-btn>

      <v-btn icon="mdi-dots-vertical">
        <v-icon icon="mdi-dots-vertical" />
        <v-menu activator="parent">
          <v-list>
            <v-list-item :to="{ name: 'accounts-logout' }"> Sair </v-list-item>
          </v-list>
        </v-menu>
      </v-btn>
    </template>
  </v-app-bar>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: false,
      default: "GFinancas",
    },
    theme: {
      type: String,
      required: true,
      default: "dark",
    },
  },
  emits: ["themeClick"],
  data() {
    return {
      currentPath: this.$route.name, // Obtém o nome da rota atual
    };
  },
  computed: {
    // Computa se a rota atual é a rota inicial
    isHomePage() {
      return this.$route.name === 'inicial'; // Nome da rota inicial
    },
  },
  methods: {
    themeClick() {
      this.$emit("themeClick")
    },
    goBack() {
      this.$router.go(-1); // Método para voltar para a página anterior
    },
  },
  watch: {
    // Atualiza a rota sempre que houver mudança
    $route(to) {
      this.currentPath = to.name;
    },
  },
}
</script>
