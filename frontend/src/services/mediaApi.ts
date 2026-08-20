import type { MediaInfo } from "../types/media"

const API_URL = "http://localhost:8000"


export async function getMediaInfo(url: string): Promise<MediaInfo> {
  const response = await fetch(`${API_URL}/api/media/info`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  })

  if (!response.ok) {
    const error = await response.json()

    throw new Error(
      error.detail || "Não foi possível analisar esta mídia."
    )
  }

  return response.json()
}


export async function downloadMedia(
  url: string,
  formatId: string,
): Promise<void> {
  const response = await fetch(`${API_URL}/api/media/download`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url,
      format_id: formatId,
    }),
  })

  if (!response.ok) {
    const error = await response.json()

    throw new Error(
      error.detail || "Não foi possível baixar esta mídia."
    )
  }

  const blob = await response.blob()

  const contentDisposition = response.headers.get(
    "Content-Disposition",
  )

  let filename = "media-download"

  if (contentDisposition) {
    const utf8Match = contentDisposition.match(
      /filename\*=utf-8''([^;]+)/i,
    )

    const regularMatch = contentDisposition.match(
      /filename="?([^"]+)"?/i,
    )

    if (utf8Match) {
      filename = decodeURIComponent(utf8Match[1])
    } else if (regularMatch) {
      filename = regularMatch[1]
    }
  }

  const objectUrl = URL.createObjectURL(blob)

  const link = document.createElement("a")

  link.href = objectUrl
  link.download = filename

  document.body.appendChild(link)

  link.click()
  link.remove()

  URL.revokeObjectURL(objectUrl)
}