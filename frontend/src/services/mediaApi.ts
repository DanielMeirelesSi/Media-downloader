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