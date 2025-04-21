<template>
  <v-card>
    <v-card-text>
      <div v-if="!hideFields">#{{ departamento.id }}</div>

      <!-- Exibição de Nome -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing">
        Nome: {{ departamento.nome }}
      </span>
      <v-text-field v-if="isEditing" v-model="editNome" label="Nome" outlined></v-text-field>
      <p></p>

      <!-- Exibição de Descrição (condicional com hideFields) -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing && !hideFields">
        Descrição: {{ departamento.description }}
      </span>
      <v-text-field v-if="isEditing && !hideFields" v-model="editDescription" label="Descrição do Departamento" outlined></v-text-field>
      <p></p>

      <!-- Exibição de Tipo Entidade (condicional com hideFields) -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing && !hideFields">
        Tipo de Entidade: {{ departamento.tipoEntidade }}
      </span>
      <v-select
        v-if="isEditing && !hideFields"
        v-model="editTipoEntidade"
        :items="tipoEntidadeOptions"
        item-value="id"
        item-text="title"
        label="Tipo de Entidade"
        outlined>
      </v-select>
      <p></p>

      <!-- Exibição do Responsável (IdUserResp) -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing">
        Responsável: {{ departamento.responsavelId ? responsavelNome : 'Não atribuído' }}
      </span>
      <v-select
        v-if="isEditing"
        v-model="editResponsavelId"
        :items="mappedUsers"
        label="Responsável"
        item-text="title"
        item-value="id"
        outlined></v-select>
      <p></p>

      <!-- Exibição de Supervisor de (Departamentos subordinados) -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing && !hideFields">
        Supervisor de: {{ departamentosSubordinados.length > 0 ? departamentosSubordinados.map(d => d.nome).join(', ') : 'Nenhum departamento' }}
      </span>
      <v-select
        v-if="isEditing && !hideFields"
        v-model="editDepartamentosSubordinados"
        :items="departamentosDisponiveis"
        label="Supervisor de"
        item-title="title"
        item-value="value"
        multiple
        chips
        outlined></v-select>
      <p></p>

      <!-- Exibição de Subordinado a (Departamento superior) -->
      <span class="ma-0 pa-0 text-h6" v-if="!isEditing && !hideFields">
        Subordinado a: {{ departamentoSuperior ? departamentoSuperior.nome : 'Nenhum departamento' }}
      </span>
      <v-select
        v-if="isEditing && !hideFields"
        v-model="editDepartamentoSuperior"
        :items="departamentosDisponiveis"
        label="Subordinado a"
        item-title="title"
        item-value="value"
        outlined></v-select>
    </v-card-text>

    <!-- Botões de Ação -->
    <v-card-actions>
      <v-btn v-if="!isEditing && !hideFields" @click="startEditing" color="primary">Editar</v-btn>
      <v-btn v-if="isEditing" @click="saveChanges" color="success">Salvar</v-btn>
      <v-btn v-if="isEditing" @click="cancelEditing" color="error">Cancelar</v-btn>
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
