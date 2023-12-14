// To accomodate varying titles and helptext for different versions
const textVersionMapping: { [key: string]: string } = {
  '0.1.0': 'default',
  '0.2.3': 'default',
  '0.3.1': 'default',
  '0.4.0': '0_4_0',
  '1.0.0': '1_0_0',
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
    localeName: 'navigation.webarchief',
    routeName: 'webarchief',
  },
  {
    localeName: 'navigation.meedoen',
    routeName: 'meedoen',
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
    localeName: 'navigation.versie-informatie',
    routeName: 'versie-informatie',
  },
]

const backendContentLanguage = 'nl'

export { textVersionMapping, keys, navigationItems, backendContentLanguage }
