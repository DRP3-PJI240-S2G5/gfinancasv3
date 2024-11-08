<template>
  <v-card>
    <v-card-text>
      <div>{{ departamento.id }}</div>
      
      <!-- Exibição de Nome -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing">
        Nome: {{ departamento.Nome }}
      </span>
      <v-text-field
        v-if="isEditing"
        v-model="editNome"
        label="Nome"
        outlined
      ></v-text-field>
      <p></p>
      
      <!-- Exibição de Descrição -->
      <span class="ma-0 pa-0 text-h5 text--primary" v-if="!isEditing">
        Descrição: {{ departamento.description }}
      </span>
      <v-text-field
        v-if="isEditing"
        v-model="editDescription"
        label="Descrição do Departamento"
        outlined
      ></v-text-field>
      <p></p>
      
      <!-- Exibição de Tipo Entidade -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing">
        Tipo de Entidade: {{ departamento.TipoEntidade }}
      </span>
      <v-text-field
        v-if="isEditing"
        v-model="editTipoEntidade"
        label="Tipo de Entidade"
        outlined
      ></v-text-field>
      <p></p>
      
      <!-- Exibição do Responsável (IdUserResp) -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing">
        Responsável: {{ departamento.IdUserResp ? responsavelNome : 'Não atribuído' }}
      </span>
      <v-select
        v-if="isEditing"
        v-model="editResponsavelId"
        :items="usuariosMapped"
        label="Responsável"
        item-text="title"
        item-value="value"
        outlined
      ></v-select>
    </v-card-text>

    <!-- Botões de Ação -->
    <v-card-actions>
      <v-btn v-if="!isEditing" @click="startEditing" color="primary">Editar</v-btn>
      <v-btn v-if="isEditing" @click="saveChanges" color="success">Salvar</v-btn>
      <v-btn v-if="isEditing" @click="cancelEditing" color="error">Cancelar</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { useAccountsStore } from "@/stores/accountsStore";
import { useCoreStore } from "@/stores/coreStore";

export default {
  name: "DepartamentosModel",
  props: {
    departamento: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      isEditing: false,
      editDescription: this.departamento.description,
      editNome: this.departamento.Nome,  
      editTipoEntidade: this.departamento.TipoEntidade, 
      editResponsavelId: this.departamento.IdUserResp || null,
    }
  },
  computed: {
    usuarios() {
      const accountsStore = useAccountsStore();
      return accountsStore.users; // Acessa a lista de usuários da store
    },
    // Mapeamento dos usuários para garantir que o v-select receba tipos simples
    usuariosMapped() {
      return this.usuarios.map(user => ({
        title: user.username,  // 'username' será mostrado no select
        value: user.id        // 'id' será o valor associado ao select
      }));
    },
    responsavelNome() {
      // Encontra o username correspondente ao IdUserResp
      const responsavel = this.usuarios.find(user => user.id === this.departamento.IdUserResp);
      return responsavel ? responsavel.username : 'Não atribuído';
    },
  },
  async created() {
    const accountsStore = useAccountsStore();
    if (accountsStore.users.length === 0) {
      try {
        await accountsStore.get_users(); // Carrega usuários
      } catch (error) {
        console.error("Erro ao carregar usuários:", error);
      }
    }
  },
  methods: {
    startEditing() {
      this.isEditing = true;
    },
    async saveChanges() {
      const coreStore = useCoreStore();
      try {
        // Envia a atualização para a API
        await useCoreStore().updateDepartamento(this.departamento.id, {
          description: this.editDescription,
          Nome: this.editNome,
          TipoEntidade: this.editTipoEntidade,
          IdUserResp: this.editResponsavelId,
        });
        
        // Atualiza os dados no componente
        this.departamento.description = this.editDescription;
        this.departamento.Nome = this.editNome;
        this.departamento.TipoEntidade = this.editTipoEntidade;
        this.departamento.responsavel = this.usuarios.find(user => user.id === this.editResponsavelId);
        
        this.isEditing = false;
        this.$emit("updated", this.departamento); // Emite o evento de atualização
      } catch (error) {
        console.error("Erro ao atualizar o departamento:", error.message); // Exibe mensagem mais detalhada
        // Exibir mensagem de erro para o usuário
        this.$notify({
          type: 'error',
          message: 'Ocorreu um erro ao salvar as alterações. Por favor, tente novamente mais tarde.'
        });
      }
    },
    cancelEditing() {
      this.isEditing = false;
      this.editDescription = this.departamento.description;
      this.editNome = this.departamento.Nome;
      this.editTipoEntidade = this.departamento.tipo_entidade;
      this.editResponsavelId = this.departamento.responsavel?.id;
    },
  },
};
</script>

<style scoped>
.v-card {
  margin: 10px;
}
</style>
