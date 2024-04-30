import axios from 'axios'

export default cachedEventHandler(
  async () => {
    const response = await axios.get(
      process.env.NUXT_PUBLIC_API_BASE_URL + '/sitemap-urls'
    )
    if (response.status !== 200) {
      return []
    }
    return response.data
  },
  {
    name: 'sitemap-dynamic-url',
    maxAge: 0, // cache URLs for 10 minutes
  }
)
