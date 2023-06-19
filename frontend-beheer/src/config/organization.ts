export interface OrganizationNames {
  [key: string]: string
}

// Only needs to be appended by names that don't fit the default string matching:
// this-is-an-id become This Is An Id.
export const organizationNames: OrganizationNames = {
  'provincie-noord-brabant': 'Provincie Noord-Brabant',
  'provincie-noord-holland': 'Provincie Noord-Holland',
  'provincie-zuid-holland': 'Provincie Zuid-Holland',
  'ministerie-fin': 'Ministerie van Financiën',
  'ministerie-ezk': 'Ministerie van Economische Zaken en Klimaat',
  'ministerie-az': 'Ministerie van Algemene Zaken',
  'ministerie-bzk': 'Ministerie van Binnenlandse Zaken en Koninkrijksrelaties',
  'ministerie-bz': 'Ministerie van Buitenlandse Zaken',
  'ministerie-def': 'Ministerie van Defensie',
  'ministerie-ienw': 'Ministerie van Infrastructuur en Waterstaat',
  'ministerie-jenv': 'Ministerie van Justitie en Veiligheid',
  'ministerie-lnw': 'Ministerie van Landbouw, Natuur en Voedselkwaliteit',
  'ministerie-ocw': 'Ministerie van Onderwijs, Cultuur en Wetenschap',
  'ministerie-szw': 'Ministerie van Sociale Zaken en Werkgelegenheid',
  'ministerie-vws': 'Ministerie van Volksgezondheid, Welzijn en Sport',
  'justitiele-informatiedienst': 'Justitiële Informatiedienst',
  rvig: 'Rijksdienst voor Identiteitsgegevens',
  'directie-financieel-economische-zaken': 'Directie Financieel-Economische Zaken',
}
