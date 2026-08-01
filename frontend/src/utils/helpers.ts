import dayjs from 'dayjs'

export function formatDate(value: string | Date) {
  return dayjs(value).format('MMM D, YYYY')
}
