import * as v0_1 from '@/layout-config/v0_1.json'
import * as v0_4 from '@/layout-config/v0_4.json'
import * as v1_0 from '@/layout-config/v1_0.json'

export default function (version: string): Record<string, any> {
  const mapping: Record<string, any> = {
    v0_1,
    v0_4,
    v1_0,
  }
  return mapping[version]
}
