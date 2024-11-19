import type { FooterColumn } from '~~/types/footer'

const footer: FooterColumn = {
  internal_col1: [
    {
      key: 'over',
      path: '/over',
    },
    {
      key: 'over_algoritmes',
      path: '/over-algoritmes',
    },
    {
      key: 'registreer-je-algoritme',
      path: '/registreer-je-algoritme',
    },
    {
      key: 'vragen',
      path: '/vragen',
    },
    {
      key: 'privacyverklaring',
      path: '/privacyverklaring',
    },
  ],
  internal_col2: [
    {
      key: 'toegankelijkheid',
      path: '/toegankelijkheid',
    },
    {
      key: 'archief',
      path: '/archief',
    },
    {
      key: 'kwetsbaarheid-melden',
      path: '/kwetsbaarheid-melden',
    },
    {
      key: 'contact',
      path: '/contact',
    },
    {
      key: 'release-notes',
      path: '/release-notes',
    },
  ],
  external: [
    {
      key: 'ext_overheid_nl',
      path: 'https://overheid.nl',
    },
    {
      key: 'ext_rijksoverheid_nl',
      path: 'https://rijksoverheid.nl',
    },
    {
      key: 'ext_digitaleoverheid_nl',
      path: 'https://digitaleoverheid.nl/overzicht-van-alle-onderwerpen/algoritmes/',
    },
    {
      key: 'ext_data_overheid_nl',
      path: 'https://data.overheid.nl',
    },
    {
      key: 'ext_pleio',
      path: 'https://algoritmes.pleio.nl/',
    },
  ],
}

export default footer
