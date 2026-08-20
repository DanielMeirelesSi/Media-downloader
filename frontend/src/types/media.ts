export interface MediaFormat {
  format_id: string
  type: string
  quality: string
  ext: string | null
  width: number | null
  height: number | null
  fps: number | null
  filesize: number | null
  has_audio: boolean
}

export interface MediaInfo {
  title: string | null
  platform: string | null
  duration: number | null
  thumbnail: string | null
  uploader: string | null
  formats: MediaFormat[]
}