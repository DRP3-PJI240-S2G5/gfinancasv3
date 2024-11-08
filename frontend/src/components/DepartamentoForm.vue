<template>
  <div>
    <v-card>
      <v-card-text>
        <!-- Campo para Nome -->
        <v-text-field
          v-model="Nome"
          label="Nome"
          required
          outlined
        />
        <!-- Campo para Descrição do Departamento -->
        <v-text-field
          v-model="description"
          label="Descrição do Departamento"
          required
          outlined
        />
        <!-- Campo para Tipo de Entidade -->
        <v-text-field
          v-model="TipoEntidade"
          label="Tipo de Entidade"
          required
          outlined
        />

        <!-- Seleção de Responsável -->
        <v-select
        v-model="IdUserResp"
        :items="usuariosMapped"
        label="Responsável"
        item-text="title"   
        item-value="value"
        outlined
        :loading="loadingUsuarios"
        :disabled="loadingUsuarios || usuarios.length === 0"
      />

        <!-- Botão para Adicionar Departamento -->
        <v-btn @click="addNewDepartamento" color="primary">Adicionar Departamento</v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { useAccountsStore } from "@/stores/accountsStore";
import { useCoreStore } from "@/stores/coreStore";

export default {
  props: {
    formLabel: {
      type: String,
      default: "",
    },
  },
  emits: ["newDepartamento"],
  data() {
    return {
      description: "",
      Nome: "",
      TipoEntidade: "",
      IdUserResp: null,
      loadingUsuarios: false, // Estado para indicar carregamento de usuários
    }
  },
  computed: {
    usuarios() {
      const accountsStore = useAccountsStore();
      return accountsStore.users; // Acessando a lista de usuários da store
    },
    // Mapeamento dos usuários para garantir que o v-select receba tipos simples
    usuariosMapped() {
      return this.usuarios.map(user => ({
        title: user.username,  // 'username' será mostrado no select
        value: user.id        // 'id' será o valor associado ao select
      }));
    },
  },
  async created() {
    const accountsStore = useAccountsStore();
    if (accountsStore.users.length === 0) {
      this.loadingUsuarios = true;
      try {
        await accountsStore.get_users(); // Carregar usuários apenas se não estiverem na store
      } catch (error) {
        console.error("Erro ao buscar usuários:", error);
      } finally {
        this.loadingUsuarios = false;
      }
    }
  },
  methods: {
    validateForm() {
      if (!this.description || !this.Nome || !this.TipoEntidade || !this.IdUserResp) {
        alert("Por favor, preencha todos os campos.");
        return false;
      }
      return true;
    },
    async addNewDepartamento() {
      const coreStore = useCoreStore();
      if (!this.validateForm()) return;

      const departamentoData = {
        description: this.description,
        Nome: this.Nome,
        TipoEntidade: this.TipoEntidade,
        IdUserResp: this.IdUserResp,
      }

      try {
        console.log("Adicionando novo dep A")
        const newDepartamento = await useCoreStore().addNewDepartamento(departamentoData);
        console.log("Adicionando novo dep F")
        // Verifique se o novo departamento foi realmente adicionado
        if (newDepartamento) {
          // Emite o evento de novo departamento
          this.$emit("newDepartamento", newDepartamento);

          // Limpar os campos após a adição
          this.description = "";
          this.Nome = "";
          this.TipoEntidade = "";
          this.IdUserResp = null;

          // Adicionar o departamento manualmente à lista para garantir que a UI seja atualizada
          this.$nextTick(() => {
            this.$emit("newDepartamento", newDepartamento);  // Envia o novo departamento para a lista na view
          });
        }
      } catch (error) {
        console.error("Erro ao adicionar departamento:", error)
      }
    },
  },
}
</script>

<style scoped></style>
