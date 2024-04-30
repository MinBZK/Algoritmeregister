import WProofreaderSDK from '@webspellchecker/wproofreader-sdk-js'

export const countWithoutHTMLTags = (fieldValue: string | null) => {
  if (!fieldValue) {
    return 0
  }
  const doc = new DOMParser().parseFromString(fieldValue, 'text/html')
  const text = doc.documentElement.textContent || ''
  return text.trim().length
}

export function toRichTextFormat(htmlTags: string[]) {
  const allowedFormatsSet = new Set<string>()
  htmlTags.forEach((tag: string) => {
    if (tag in htmlTagFormatMap) {
      const format = htmlTagFormatMap[tag]
      allowedFormatsSet.add(JSON.stringify({
        class: format!.class,
        type: format!.type,
      }))
    }
  })
  return Array.from(allowedFormatsSet, text => JSON.parse(text))
}

export interface Format {
  class: string
  type: string
}

const htmlTagFormatMap: Record<string, Format> = {
  em: { class: 'italic', type: '' },
  i: { class: 'italic', type: '' },
  strong: { class: 'bold', type: '' },
  b: { class: 'bold', type: '' },
  ul: { class: 'list', type: 'bullet' },
  ol: { class: 'list', type: 'ordered' },
}

export const initSpellchecker = (editorElement: HTMLElement) => {
  WProofreaderSDK.init({
    'container': editorElement,
    'autoDestroy': true,
    'autocorrect': false,
    'autocomplete': true,
    'disableOptionsStorage': [
      'autocorrect',
    ],
    'enforceAI': false,
    'serviceId': 'LcJrweLQQxt0p4K',
    'serviceProtocol': 'https',
    'servicePort': '443',
    'serviceHost': 'svc.webspellchecker.net',
    'servicePath': 'api',
    'lang': 'nl_NL',
    'theme': 'default',
    'localization': 'nl',
    'enableBadgeButton': true,
    'globalBadge': false,
    'enableLanguagesInBadgeButton': false,
    'actionItems': [
      'ignoreAll',
      // "ignore",
      // "proofreadDialog",
      // "addWord",
    ],
    'settingsSections': [],
  })
}
