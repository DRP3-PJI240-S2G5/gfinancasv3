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
    const { users } = storeToRefs(accountStore);

    onMounted(() => {
      accountStore.getUsers(); // Carrega os usuários ao montar o componente
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

    // Obter o nome do responsável com base no ID
    const responsavelNome = computed(() => {
      const responsavel = users.value.find(user => user.id === props.departamento.responsavelId);
      return responsavel ? responsavel.username : "Não atribuído";
    });

    // Métodos para controlar a edição
    const startEditing = () => {
      isEditing.value = true;
    };

    const saveChanges = () => {
      const updatedDepartamento = {
        id: props.departamento.id,
        nome: editNome.value,
        description: editDescription.value,
        tipoEntidade: editTipoEntidade.value,
        responsavelId: editResponsavelId.value,
        done: props.departamento.done,
      };
      emit("updateDepartamento", updatedDepartamento);
      isEditing.value = false;
    };

    const cancelEditing = () => {
      isEditing.value = false;
      // Restaurar valores originais do departamento
      editNome.value = props.departamento.nome;
      editDescription.value = props.departamento.description;
      editTipoEntidade.value = props.departamento.tipoEntidade;
      editResponsavelId.value = props.departamento.responsavelId;
      editDone.value = props.departamento.done;
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
    };
  },
};
</script>
