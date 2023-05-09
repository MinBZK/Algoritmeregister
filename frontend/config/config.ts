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

const columnGrouping = [
  {
    label: 'algemeneInformatie',
    group: [
      'name',
      'organization',
      'department',
      'description_short',
      'type',
      'category',
      'website',
      'status',
    ],
  },
  {
    label: 'inzet',
    group: [
      'goal',
      'impact',
      'proportionality',
      'decision_making_process',
      'documentation',
    ],
  },
  {
    label: 'juridisch',
    group: [
      'competent_authority',
      'lawful_basis',
      'iama',
      'iama_description',
      'dpia',
      'dpia_description',
      'objection_procedure',
    ],
  },
  {
    label: 'metadata_algorithm',
    group: ['url', 'contact_email', 'area', 'lang', 'revision_date'],
  },
  {
    label: 'toepassing',
    group: [
      'description',
      'application_url',
      'publiccode',
      'mprd',
      'source_data',
      'methods_and_models',
    ],
  },
  {
    label: 'toezicht',
    group: [
      'monitoring',
      'human_intervention',
      'risks',
      'performance_standard',
    ],
  },
]

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

const backendContentLanguage = 'nl'

export {
  columnGrouping,
  summaryTiles,
  keys,
  navigationItems,
  backendContentLanguage,
}
