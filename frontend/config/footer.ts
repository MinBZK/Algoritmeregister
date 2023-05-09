import type { FooterColumn } from '~~/types/footer'

const footer: FooterColumn = {
  internal: [
    {
      key: 'over',
      path: '/over',
    },
    {
      key: 'contact',
      path: '/contact',
    },
    {
      key: 'vragen',
      path: '/vragen',
    },
    {
      key: 'privacyverklaring',
      path: '/privacyverklaring',
    },
    {
      key: 'toegankelijkheid',
      path: '/toegankelijkheid',
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
