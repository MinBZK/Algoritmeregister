import type { FooterColumn } from '~~/types/footer'

const footer: FooterColumn[] = [
  {
    key: 'service',
    title: '',
    pages: [
      {
        label: '',
        path: '/contact',
      },
      {
        label: '',
        path: '/over',
      },
      {
        label: '',
        path: '/vragen',
      },
    ],
  },
  {
    key: 'over',
    title: '',
    pages: [
      {
        label: '',
        path: '/privacyverklaring',
      },
      // {
      //   label: '',
      //   path: '/cookies',
      // },
      // {
      //   label: ' melden',
      //   path: '/kwetsbaarheid',
      // },
      {
        label: '',
        path: '/toegankelijkheid',
      },
    ],
  },
]

export default footer
