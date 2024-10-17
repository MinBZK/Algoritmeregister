import type { OrganisationPage } from '~~/types/organisation'

export const useOrganisation = () => {
  const organisation = useState<OrganisationPage | null>(
    'organisation',
    () => null
  )
  const setOrganisation = (a: OrganisationPage | null) =>
    (organisation.value = a)

  const route = useRoute()
  watch(
    () => route.name,
    () => {
      if (!route.name?.toString().includes('organisatie-orgCode'))
        setOrganisation(null)
    }
  )

  return {
    organisation,
    setOrganisation,
  }
}
