<template>
  <q-page class="flex flex-center">
    <q-page padding class="flex justify-center items-start q-pt-xl">
      <q-stepper v-model="step" ref="stepper" alternative-labels animated
        class="shadow-2 rounded-borders q-mt-md q-pa-md">
        <q-step :name="0" :title="$t('LABEL_ENTER_INFO')" active-icon="fa-solid fa-plus" icon="fa-solid fa-plus">
          <div class="input-container q-gutter-lg">
            <div class="text-h6">{{ $t('TEXT_SINGUP_EMAIL') }}</div>
            <q-input no-error-icon filled :placeholder="$t('LABEL_EMAIL')" name='email' maxlength="100" class="email text-h6"
              v-model="email"></q-input>
            <q-toggle v-model="accept" :label="$t('TEXT_ACCEPT_LICENSE')"></q-toggle>
            <q-stepper-navigation class="flex items-start justify-end q-pt-md">
              <q-btn @click="stepperNext" :loading="noNext" color="primary" :label="$t('BTN_CONTINUE')" class="btn-fixed-width">
              </q-btn>
            </q-stepper-navigation>
          </div>
        </q-step>
        <q-step :name="1" :title="$t('LABEL_VERIFY_IDENTITY')" active-icon="fa-solid fa-check" icon="fa-solid fa-check">
          <div class="input-container q-gutter-lg">
            <div>
              <div class="text-h6">{{ $t('TEXT_ENTER_VERIFICATION_CODE') }}</div>
              <div class="text-subtitle1">{{ $t('TEXT_SECURE_LINK_VERIFIED') }}</div>
            </div>
            <q-form id="verifyForm" action="/auth/verify" method="post">
              <q-input v-model="verifyCode" name="verifyCode" bg-color="grey-2" filled mask="#####" autofocus class="text-h4 auth-code">
              </q-input>
              <input type="hidden" name="resource" v-model="resource" />
            </q-form>
            <q-stepper-navigation class="flex items-start justify-between q-pt-md">
              <q-btn color="primary" @click="$refs.stepper.previous()" outline :label="$t('BTN_BACK')" class="btn-fixed-width">
              </q-btn>
              <q-btn @click="stepperDone" :loading="noNext" color="primary" :label="$t('BTN_DONE')" class="btn-fixed-width">
              </q-btn>
            </q-stepper-navigation>
          </div>
        </q-step>
      </q-stepper>
    </q-page>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useI18n } from 'vue-i18n'
import { api } from 'src/boot/api'

export default defineComponent({
  name: 'IndexPage',
  setup () {
    const $q = useQuasar()
    const { t } = useI18n()

    // TODO delete email
    const email = ref('yugan6688@gmail.com')
    const verifyCode = ref(null)
    const noNext = ref(false)
    const accept = ref(false)
    const step = ref(0)

    const resource = ref(useRouter().currentRoute.value.path.split('/').pop())
    const resourceUrl = ref(null)

    function stepperNext () {
      let checkOk = true
      step.value = 1
      if (!/^[^@]+@[^@]+\.[^@]+$/.test(email.value)) {
        checkOk = false
        $q.notify({
          color: 'red-5',
          position: 'top',
          icon: 'fa-solid fa-exclamation',
          message: t('MSG_NOT_VALID_EMAIL')
        })
      }

      if (accept.value !== true) {
        checkOk = false
        $q.notify({
          color: 'red-5',
          position: 'top',
          icon: 'fa-solid fa-exclamation',
          message: t('MSG_NOT_ACCEPT_LICENSE')
        })
      }

      if (checkOk) {
        noNext.value = true
        api.post('auth/signup', { email: email.value, resource: resource.value },
          { withCredentials: false }).then(function (response) {
          if (response.data.code === 'I005') {
            $q.notify({
              color: 'red-5',
              position: 'top',
              icon: 'fa-solid fa-exclamation',
              message: t('MSG_HAS_SIGNED_EMAIL')
            })
          } else if (response.data.code === 'I001') {
            verifyCode.value = null
            step.value = 1
          }
          noNext.value = false
        }).catch(function (error) {
          noNext.value = false
          console.log(error)
        })
      }
    }
    function stepperDone () {
      noNext.value = true
      api.post('auth/verify/check', {
        email: email.value,
        verifyCode: verifyCode.value
      }).then(function (response) {
        if (response.data.code === 'I003') {
          document.querySelector('#verifyForm').submit()
        } else if (response.data.code === 'I004') {
          $q.notify({
            color: 'red-5',
            position: 'top',
            icon: 'fa-solid fa-exclamation',
            message: t('MSG_VERIFY_CODE_WRONG')
          })
        } else if (response.data.code === 'I007') {
          $q.notify({
            color: 'red-5',
            position: 'top',
            icon: 'fa-solid fa-exclamation',
            message: t('MSG_VERIFY_CODE_TIMEOUT')
          })
        }
        noNext.value = false
      }).catch(function () {
        step.value = 0
        noNext.value = false
      })
    }
    return {
      email,
      accept,
      verifyCode,
      step,
      stepperNext,
      noNext,
      stepperDone,
      resourceUrl,
      resource
    }
  }
})
</script>
<style>
/* Extra small devices (phones, 600px and down) */
@media only screen and (max-width: 600px) {
  .input-container, .success-container {
    width: 300px;
    min-height: 260px;
    padding-left: 0px;
  }
}
@media only screen and (min-width: 1000px) {
  .input-container, .success-container {
    min-width: 600px;
    min-height: 260px;
    padding-left: 60px;
  }
}
.success-container {
  text-align: center;
}
.email {
    max-width: 420px;
}
.auth-code {
    max-width: 200px;
}
.auth-code input {
    letter-spacing: 8px;
    text-align: center;
}
.btn-fixed-width {
    width: 120px;
}
</style>
