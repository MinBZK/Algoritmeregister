export type FooterPage = {
  label: string
  path: string
}

export type FooterColumn = {
  key: string
  title: string
  pages: FooterPage[]
}

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
      {
        label: '',
        path: '/cookies',
      },
      {
        label: ' melden',
        path: '/kwetsbaarheid',
      },
      {
        label: '',
        path: '/toegankelijkheid',
      },
    ],
  },
]

export default footer
