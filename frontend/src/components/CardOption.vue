<template>
  <v-card class="mx-auto" max-width="400" hover link>
    <v-card-title class="headline"> {{ cardOptionTitle }} </v-card-title>
    <v-card-text>
      {{ cardOptionDescription }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'CardOption',
  props: {
    cardOptionTitle: {
      type: String,
      required: true
    },
    cardOptionDescription: {
      type: String,
      required: true
    }
  }
}
</script>
