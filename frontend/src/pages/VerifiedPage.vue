<template>
  <q-page class="flex flex-center">
    <q-page padding class="flex justify-center items-start q-pt-xl">
      <div v-if="verifySuccess" class="success-container shadow-2 rounded-borders q-mt-xl q-pa-xl q-gutter-lg">
        <q-icon name="fa-regular fa-circle-check" color="positive" size="120px"/>
        <div>
          <div class="text-h6">Your email has been successfully verifyed.</div>
          <div class="text-subtitle1">Click the botton blow to proceed to you page.</div>
        </div>
        <q-btn :href="resourceUrl" class="q-px-xl q-py-xs text-h6 q-mb-xl" color="primary" label="To my page"/>
      </div>
    </q-page>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'VerifySuccessPage',
  props: {
    accessToken: {
      type: String,
      required: true
    },
    refreshToken: {
      type: String,
      required: true
    }
  },
  setup () {

  }
})
</script>
<style>

</style>
