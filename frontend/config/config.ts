// To accomodate varying titles and helptext for different versions
const textVersionMapping: { [key: string]: string } = {
  '0.1': 'default',
  '0.4': '0_4',
  '1.0': '1_0',
}

const keys = {
  id: 'id',
  name: 'name',
  description: 'description_short',
  organisation: 'organization',
  department: 'department',
  type: 'type',
  theme: 'category',
  status: 'status',
}

const navigationItems = [
  {
    localeName: 'navigation.home',
    routeName: ' ',
  },
  {
    localeName: 'navigation.algorithmRegister',
    routeName: 'algoritme',
  },
  {
    localeName: 'navigation.footer',
    routeName: 'footer',
  },
  {
    localeName: 'navigation.over',
    routeName: 'over',
  },
  {
    localeName: 'navigation.contact',
    routeName: 'contact',
  },
  {
    localeName: 'navigation.vragen',
    routeName: 'vragen',
  },
  {
    localeName: 'navigation.privacyverklaring',
    routeName: 'privacyverklaring',
  },
  {
    localeName: 'navigation.toegankelijkheid',
    routeName: 'toegankelijkheid',
  },
  {
    localeName: 'navigation.archief',
    routeName: 'archief',
  },
  {
    localeName: 'navigation.kwetsbaarheid-melden',
    routeName: 'kwetsbaarheid-melden',
  },
  {
    localeName: 'navigation.over-algoritmes',
    routeName: 'over-algoritmes',
  },
  {
    localeName: 'navigation.db',
    routeName: 'dashboard',
  },
  {
    localeName: 'navigation.release-notes',
    routeName: 'release-notes',
  },
  {
    localeName: 'navigation.organisatie',
    routeName: 'organisatie',
  },
  {
    localeName: 'navigation.registreer-je-algoritme',
    routeName: 'registreer-je-algoritme',
  },
  {
    localeName: 'navigation.copyright',
    routeName: 'copyright',
  },
  {
    localeName: 'navigation.cookies',
    routeName: 'cookies',
  },
  {
    localeName: 'navigation.sitemap',
    routeName: 'sitemap',
  },
  {
    localeName: 'navigation.organisatie-niet-aangesloten',
    routeName: 'organisatie-niet-aangesloten',
  },
  {
    localeName: 'navigation.organisatie-niet-gepubliceerd',
    routeName: 'organisatie-niet-gepubliceerd',
  },
]

const backendContentLanguage = 'nl'

export { textVersionMapping, keys, navigationItems, backendContentLanguage }
