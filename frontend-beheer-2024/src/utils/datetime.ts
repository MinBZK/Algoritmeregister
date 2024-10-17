export const formatDateTime = (datetime: Date | string): string => {
  // Date formatted as 'dd-MM-yyyy hh:mm' in 24-hour format
  const date = new Date(datetime)
  const day = date.getDate()
  const month = date.getMonth() + 1
  const year = date.getFullYear()
  const hours = date.getHours()
  const minutes = date.getMinutes()
  return `${day}-${month}-${year} ${hours}:${minutes}`
}

export const formatDate = (datetime: Date | string): string => {
  // Date formatted as 'dd-MM-yyyy hh:mm' in 24-hour format
  const date = new Date(datetime)
  const day = date.getDate()
  const month = date.getMonth() + 1
  const year = date.getFullYear()
  return `${day}-${month}-${year}`
}
