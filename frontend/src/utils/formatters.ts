export function formatDuration(
  seconds: number | null,
): string | null {
  if (seconds === null || !Number.isFinite(seconds)) {
    return null
  }

  const totalSeconds = Math.max(0, Math.floor(seconds))

  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const remainingSeconds = totalSeconds % 60

  if (hours > 0) {
    return [
      hours,
      String(minutes).padStart(2, "0"),
      String(remainingSeconds).padStart(2, "0"),
    ].join(":")
  }

  return [
    minutes,
    String(remainingSeconds).padStart(2, "0"),
  ].join(":")
}


export function formatFileSize(
  bytes: number | null,
): string | null {
  if (bytes === null || bytes <= 0) {
    return null
  }

  const kilobytes = bytes / 1024
  const megabytes = kilobytes / 1024
  const gigabytes = megabytes / 1024

  if (gigabytes >= 1) {
    return `${gigabytes.toFixed(2)} GB`
  }

  if (megabytes >= 1) {
    return `${megabytes.toFixed(1)} MB`
  }

  return `${Math.round(kilobytes)} KB`
}