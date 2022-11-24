export type FooterPage = {
  label: string
  slug: string
}

export type FooterColumn = {
  title: string
  pages: FooterPage[]
}

const footer: FooterColumn[] = [
  {
    title: 'Service',
    pages: [
      {
        label: 'Contact',
        slug: 'contact',
      },
      {
        label: 'Over',
        slug: 'over',
      },
    ],
  },
  {
    title: 'Over deze site',
    pages: [
      {
        label: 'Privacyverklaring',
        slug: 'privacyverklaring',
      },
    ],
  },
]

export default footer
