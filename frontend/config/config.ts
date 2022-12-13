const summaryTiles: Array<string> = [
  'organization',
  'department',
  'category',
  'type',
  'status',
]

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
    localeName: 'navigation.db',
    routeName: 'dashboard',
  },
]

export { summaryTiles, keys, navigationItems }
