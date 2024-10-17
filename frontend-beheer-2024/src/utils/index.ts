import { NoOrgResponse } from '@/types/algorithm'
import { notifications } from '@/config/notifications'
import { useSnackbarStore } from '@/store/snackbar'

export function noOrgSelectedResponse(): NoOrgResponse {
  const { add: addNotification } = useSnackbarStore()
  addNotification(notifications.noOrgSelectedError!)
  return { status: 400, data: null }
}

export function unknownError() {
  const { add: addNotification } = useSnackbarStore()
  addNotification(notifications.unknownError!)
}

export const arrayToggleValue = (
  array: string[],
  toggle: boolean,
  value: string
): string[] => {
  // Remove value from array when toggle is false, Add to array when true.
  if (toggle) {
    const newArray = [...array]
    newArray.push(value)
    return Array.from(new Set(newArray))
  } else {
    return array.filter((c) => c !== value)
  }
}
