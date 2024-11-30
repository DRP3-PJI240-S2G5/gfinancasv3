<template>
  <v-container>
    <v-card>
      <v-card-title class="text-overline">
        {{ departamento.nome }}

        <div class="text-green-darken-3 text-h3 font-weight-bold">90%</div>

        <div class="text-h6 text-medium-emphasis font-weight-regular">
          $2,938.00 restante
        </div>
      </v-card-title>
      <br>
      <v-card-text>
        <div
          :style="`right: calc(${review} - 0px)`"
          class="position-absolute mt-n8 text-caption text-green-darken-3"
        >
          Meta
        </div>
        <v-progress-linear
          color="green-darken-3"
          height="22"
          model-value="90"
          rounded="lg"
        >
          <v-badge
            :style="`right: ${review}`"
            class="position-absolute"
            color="white"
            dot
            inline
          ></v-badge>
        </v-progress-linear>

        <div class="d-flex justify-space-between py-3">
          <span class="text-green-darken-3 font-weight-medium">
            $26,442.00<br>gastos e despesas
          </span>

          <span class="text-medium-emphasis"> $29,380.00<br>verba total </span>
        </div>
      </v-card-text>

      <v-divider></v-divider>

      <v-list-item
        append-icon="mdi-chevron-right"
        lines="two"
        subtitle="Detalhes"
        link
        @click="toggleDetails"
      ></v-list-item>

      <v-expand-transition>
        <div v-show="isActive">
          <v-list dense>
            <v-list-item
              v-for="expense in departamento.gastos"
              :key="expense.id"
            >
              <v-list-item>
                <v-list-item-title>{{ expense.descricao }}</v-list-item-title>
                <v-list-item-subtitle>
                  R$ {{ expense.valor.toFixed(2) }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list-item>
          </v-list>
        </div>
      </v-expand-transition>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data: () => ({ review: "30%" }),
  props: {
    departamento: {
      type: Object,
      required: true,
    },
    isActive: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    toggleDetails() {
      this.$emit("toggle-department", this.departamento.id);
    },
  },
};
</script>
