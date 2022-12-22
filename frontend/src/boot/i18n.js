import { createI18n } from 'vue-i18n'
import messages from 'src/i18n'
import { Quasar } from 'quasar'

export default ({ app }) => {
  // Create I18n instance
  const i18n = createI18n({
    locale: Quasar.lang.getLocale(),
    globalInjection: true,
    legacy: false,
    silentTranslationWarn: true,
    silentFallbackWarn: true,
    fallbackLocale: 'en-US',
    messages
  })
  app.use(i18n)
}
