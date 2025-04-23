<template>
  <v-card class="mb-4" elevation="2">
    <v-card-text>
      <div v-if="!hideFields" class="text-subtitle-1 font-weight-bold mb-2">#{{ departamento.id }}</div>

      <!-- Exibição de Nome -->
      <div class="field-container mb-3">
        <div class="field-row">
          <div class="field-label font-weight-bold text-subtitle-1">Nome:</div>
          <div v-if="!isEditing" class="field-value">{{ departamento.nome }}</div>
          <v-text-field v-if="isEditing" v-model="editNome" label="Nome" outlined dense class="field-input"></v-text-field>
        </div>
      </div>

      <!-- Exibição de Descrição (condicional com hideFields) -->
      <div v-if="!hideFields" class="field-container mb-3">
        <div class="field-row">
          <div class="field-label font-weight-bold text-subtitle-1">Descrição:</div>
          <div v-if="!isEditing" class="field-value">{{ departamento.description }}</div>
          <v-text-field v-if="isEditing" v-model="editDescription" label="Descrição do Departamento" outlined dense class="field-input"></v-text-field>
        </div>
      </div>

      <!-- Exibição de Tipo Entidade (condicional com hideFields) -->
      <div v-if="!hideFields" class="field-container mb-3">
        <div class="field-row">
          <div class="field-label font-weight-bold text-subtitle-1">Tipo de Entidade:</div>
          <div v-if="!isEditing" class="field-value">{{ departamento.tipoEntidade }}</div>
          <v-select
            v-if="isEditing"
            v-model="editTipoEntidade"
            :items="tipoEntidadeOptions"
            item-value="id"
            item-text="title"
            label="Tipo de Entidade"
            outlined
            dense
            class="field-input">
          </v-select>
        </div>
      </div>

      <!-- Exibição do Responsável (IdUserResp) -->
      <div class="field-container mb-3">
        <div class="field-row">
          <div class="field-label font-weight-bold text-subtitle-1">Responsável:</div>
          <div v-if="!isEditing" class="field-value">{{ departamento.responsavelId ? responsavelNome : 'Não atribuído' }}</div>
          <v-select
            v-if="isEditing"
            v-model="editResponsavelId"
            :items="mappedUsers"
            label="Responsável"
            item-text="title"
            item-value="id"
            outlined
            dense
            class="field-input"></v-select>
        </div>
      </div>

      <!-- Exibição de Supervisor de (Departamentos subordinados) -->
      <div v-if="!hideFields" class="field-container mb-3">
        <div class="field-row">
          <div class="field-label font-weight-bold text-subtitle-1">Supervisor de:</div>
          <div v-if="!isEditing" class="field-value">{{ departamentosSubordinados.length > 0 ? departamentosSubordinados.map(d => d.nome).join(', ') : 'Nenhum departamento' }}</div>
          <v-select
            v-if="isEditing"
            v-model="editDepartamentosSubordinados"
            :items="departamentosDisponiveis"
            label="Supervisor de"
            item-title="title"
            item-value="value"
            multiple
            chips
            outlined
            dense
            class="field-input"></v-select>
        </div>
      </div>

      <!-- Exibição de Subordinado a (Departamento superior) -->
      <div v-if="!hideFields" class="field-container mb-3">
        <div class="field-row">
          <div class="field-label font-weight-bold text-subtitle-1">Subordinado a:</div>
          <div v-if="!isEditing" class="field-value">{{ departamentoSuperior ? departamentoSuperior.nome : 'Nenhum departamento' }}</div>
          <v-select
            v-if="isEditing"
            v-model="editDepartamentoSuperior"
            :items="departamentosDisponiveis"
            label="Subordinado a"
            item-title="title"
            item-value="value"
            outlined
            dense
            class="field-input"></v-select>
        </div>
      </div>
    </v-card-text>

    <!-- Botões de Ação -->
    <v-card-actions class="pa-4">
      <v-btn 
        v-if="!isEditing && !hideFields" 
        @click="startEditing" 
        color="primary" 
        class="mr-2"
        elevation="2">
        <v-icon left>mdi-pencil</v-icon>
        Editar
      </v-btn>
      <v-btn 
        v-if="isEditing" 
        @click="saveChanges" 
        color="success" 
        class="mr-2"
        elevation="2">
        <v-icon left>mdi-check</v-icon>
        Salvar
      </v-btn>
      <v-btn 
        v-if="isEditing" 
        @click="cancelEditing" 
        color="error"
        elevation="2">
        <v-icon left>mdi-close</v-icon>
        Cancelar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { useAccountsStore } from "@/stores/accountsStore";
import { useCoreStore } from "@/stores/coreStore";
import { ref, computed, onMounted } from "vue";
import { storeToRefs } from "pinia";

export default {
  props: {
    departamento: {
      type: Object,
      required: true,
    },
    hideFields: {
      type: Boolean,
      default: false, // Por padrão, os campos são visíveis
    },
  },
  emits: ["updateDepartamento"],
  setup(props, { emit }) {
    const accountStore = useAccountsStore();
    const coreStore = useCoreStore();
    const { users } = storeToRefs(accountStore);
    const { departamentos, subordinacoes } = storeToRefs(coreStore);

    onMounted(async () => {
      accountStore.getUsers(); // Carrega os usuários ao montar o componente
      await coreStore.getSubordinacoes(); // Carrega as subordinações
    });

    const mappedUsers = computed(() => {
      return users.value.map(user => ({
        title: user.username,
        id: user.id,
      }));
    });

    // Dados do departamento editável
    const isEditing = ref(false);
    const editNome = ref(props.departamento.nome);
    const editDescription = ref(props.departamento.description);
    const editTipoEntidade = ref(props.departamento.tipoEntidade);
    const editResponsavelId = ref(props.departamento.responsavelId);
    const tipoEntidadeOptions = ref(["Tipo A", "Tipo B", "Tipo C"]);
    const editDone = ref(props.departamento.done);
    
    // Campos para subordinação
    const editDepartamentosSubordinados = ref([]);
    const editDepartamentoSuperior = ref(null);

    // Obter o nome do responsável com base no ID
    const responsavelNome = computed(() => {
      const responsavel = users.value.find(user => user.id === props.departamento.responsavelId);
      return responsavel ? responsavel.username : "Não atribuído";
    });

    // Departamentos disponíveis para seleção (excluindo o departamento atual)
    const departamentosDisponiveis = computed(() => {
      return departamentos.value
        .filter(d => d.id !== props.departamento.id)
        .map(dep => ({
          title: dep.nome,
          value: dep.id
        }));
    });

    // Departamentos subordinados (onde este departamento é o superior)
    const departamentosSubordinados = computed(() => {
      const subordinacoesAtuais = subordinacoes.value.filter(
        s => s.superior.id === props.departamento.id
      );
      return subordinacoesAtuais.map(s => s.subordinado);
    });

    // Departamento superior (onde este departamento é o subordinado)
    const departamentoSuperior = computed(() => {
      const subordinacao = subordinacoes.value.find(
        s => s.subordinado.id === props.departamento.id
      );
      return subordinacao ? subordinacao.superior : null;
    });

    // Métodos para controlar a edição
    const startEditing = () => {
      isEditing.value = true;
      
      // Inicializar os campos de subordinação
      editDepartamentosSubordinados.value = departamentosSubordinados.value.map(d => d.id);
      editDepartamentoSuperior.value = departamentoSuperior.value ? departamentoSuperior.value.id : null;
    };

    const saveChanges = async () => {
      const updatedDepartamento = {
        id: props.departamento.id,
        nome: editNome.value,
        description: editDescription.value,
        tipoEntidade: editTipoEntidade.value,
        responsavelId: editResponsavelId.value,
        done: props.departamento.done,
      };
      
      // Primeiro, atualizar o departamento
      await emit("updateDepartamento", updatedDepartamento);
      
      // Depois, gerenciar as subordinações
      await gerenciarSubordinacoes();
      
      isEditing.value = false;
    };

    const gerenciarSubordinacoes = async () => {
      try {
        // 1. Remover subordinações existentes onde este departamento é o superior
        const subordinacoesExistentes = subordinacoes.value.filter(
          s => s.superior.id === props.departamento.id
        );
        
        for (const sub of subordinacoesExistentes) {
          // Se o departamento subordinado não está mais na lista, remover a subordinação
          if (!editDepartamentosSubordinados.value.includes(sub.subordinado.id)) {
            await coreStore.deleteSubordinacao(sub.id);
          }
        }
        
        // 2. Adicionar novas subordinações onde este departamento é o superior
        for (const subordinadoId of editDepartamentosSubordinados.value) {
          // Verificar se já existe uma subordinação
          const existe = subordinacoes.value.some(
            s => s.superior.id === props.departamento.id && s.subordinado.id === subordinadoId
          );
          
          if (!existe) {
            await coreStore.createSubordinacao({
              IdDepartamentoA: props.departamento.id,
              IdDepartamentoB: subordinadoId
            });
          }
        }
        
        // 3. Gerenciar a subordinação onde este departamento é o subordinado
        const subordinacaoExistente = subordinacoes.value.find(
          s => s.subordinado.id === props.departamento.id
        );
        
        // Se existe uma subordinação e o superior foi alterado ou removido
        if (subordinacaoExistente && 
            (subordinacaoExistente.superior.id !== editDepartamentoSuperior.value || 
             !editDepartamentoSuperior.value)) {
          await coreStore.deleteSubordinacao(subordinacaoExistente.id);
        }
        
        // Se um novo superior foi selecionado e não existe subordinação
        if (editDepartamentoSuperior.value && 
            (!subordinacaoExistente || 
             subordinacaoExistente.superior.id !== editDepartamentoSuperior.value)) {
          await coreStore.createSubordinacao({
            IdDepartamentoA: editDepartamentoSuperior.value,
            IdDepartamentoB: props.departamento.id
          });
        }
        
        // Atualizar a lista de subordinações
        await coreStore.getSubordinacoes();
      } catch (error) {
        console.error("Erro ao gerenciar subordinações:", error);
      }
    };

    const cancelEditing = () => {
      isEditing.value = false;
      // Restaurar valores originais do departamento
      editNome.value = props.departamento.nome;
      editDescription.value = props.departamento.description;
      editTipoEntidade.value = props.departamento.tipoEntidade;
      editResponsavelId.value = props.departamento.responsavelId;
      editDone.value = props.departamento.done;
      
      // Restaurar valores originais das subordinações
      editDepartamentosSubordinados.value = departamentosSubordinados.value.map(d => d.id);
      editDepartamentoSuperior.value = departamentoSuperior.value ? departamentoSuperior.value.id : null;
    };

    return {
      isEditing,
      editNome,
      editDescription,
      editTipoEntidade,
      editResponsavelId,
      tipoEntidadeOptions,
      mappedUsers,
      responsavelNome,
      startEditing,
      saveChanges,
      cancelEditing,
      departamentosDisponiveis,
      departamentosSubordinados,
      departamentoSuperior,
      editDepartamentosSubordinados,
      editDepartamentoSuperior,
    };
  },
};
</script>

<style scoped>
.field-container {
  display: flex;
  flex-direction: column;
}

.field-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.field-label {
  color: #1976d2;
  margin-right: 16px;
  min-width: 120px;
}

.field-value {
  font-size: 1.1rem;
  flex: 1;
}

.field-input {
  flex: 1;
}

.v-card {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.v-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
}

.v-btn {
  text-transform: none;
  font-weight: 500;
}
</style>
