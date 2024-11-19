import { useI18n } from 'vue-i18n'

export function useGeotopLegendData() {
  const { t } = useI18n()

  const geotopLegendData = [
    {
      title: t('dashboard.legendGreen'),
      colour: 'rgba(85, 177, 165, 0.8)',
      className: 'legendgreen-background',
    },
    {
      title: t('dashboard.legendYellow'),
      colour: 'rgba(237, 208, 136, 0.8)',
      className: 'legendyellow-background',
    },
    {
      title: t('dashboard.legendWhite'),
      colour: 'rgba(255, 0, 0, 0.0)',
      className: 'legendwhite-background',
    },
  ]

  return geotopLegendData
}
