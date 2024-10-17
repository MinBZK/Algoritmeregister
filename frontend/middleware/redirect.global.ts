import type { Algoritme } from '@/types/algoritme'
import algoritmeService from '@/services/algoritme'
import type { LanguageCode } from '@/types/textLoader'

const slugFromAlgo = (algoritme?: Algoritme): string => {
  const name = algoritme?.name
  const org = algoritme?.organization
  let slug = name?.toLowerCase() + ' ' + org?.toLowerCase()
  slug = slug.replaceAll(/[^a-zA-Z0-9 ]/g, '')
  // Some names have two spaces, the following line ensures this does not become '--'.
  slug = slug.replaceAll('  ', '-')
  slug = slug.replaceAll(' ', '-')
  return slug
}

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Handles algorithm detail page and constructing the slug
  if (to.params.slug) {
    const locale = to.path.split('/')[1] as LanguageCode
    const lars = (to.params.lars || to.params.slug) as string
    if (lars.includes('C')) return

    // Retrieve algoritme here to build slug. Store it globally so don't have to get it again
    const algoritme = useState<Algoritme | null>('algoritme', () => null)
    if (
      !algoritme.value ||
      algoritme.value.lars !== lars ||
      locale !== from.path.split('/')[1]
    ) {
      const { data } = await algoritmeService.getOne(
        lars,
        mapLocaleName(locale)
      )
      algoritme.value = data.value as Algoritme
    }

    const slug = slugFromAlgo(algoritme.value)
    if (slug === to.params.slug) return

    return navigateTo({
      path: `/${locale}/algoritme/${slug}/${lars}`,
    })
  }
})
