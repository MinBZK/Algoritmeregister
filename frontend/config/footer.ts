import type { FooterColumn } from '~~/types/footer'

const footer: FooterColumn[] = [
  {
    key: 'service',
    title: '',
    pages: [],
  },
  {
    key: 'over',
    title: '',
    pages: [
      {
        label: '',
        path: '/privacyverklaring',
      },
      {
        label: '',
        path: '/toegankelijkheid',
      },
      {
        label: '',
        path: '/over',
      },
      {
        label: '',
        path: '/vragen',
      },
      {
        label: '',
        path: '/contact',
      },
      // {
      //   label: '',
      //   path: '/cookies',
      // },
      // {
      //   label: ' melden',
      //   path: '/kwetsbaarheid',
      // },
    ],
  },
]

export default footer
