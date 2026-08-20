import { useState } from "react"

import "./App.css"

import {
  downloadMedia,
  getMediaInfo,
} from "./services/mediaApi"

import type { MediaInfo } from "./types/media"

import {
  formatDuration,
  formatFileSize,
} from "./utils/formatters"


function App() {
  const [url, setUrl] = useState("")
  const [media, setMedia] = useState<MediaInfo | null>(null)

  const [loading, setLoading] = useState(false)
  const [downloadingFormat, setDownloadingFormat] =
    useState<string | null>(null)

  const [error, setError] = useState<string | null>(null)


  async function handleAnalyze() {
    if (!url.trim()) {
      setError("Cole um link para continuar.")
      return
    }

    setLoading(true)
    setError(null)
    setMedia(null)

    try {
      const result = await getMediaInfo(url)
      setMedia(result)
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError("Ocorreu um erro inesperado.")
      }
    } finally {
      setLoading(false)
    }
  }


  async function handleDownload(formatId: string) {
    try {
      setDownloadingFormat(formatId)
      setError(null)

      await downloadMedia(url, formatId)
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError("Ocorreu um erro durante o download.")
      }
    } finally {
      setDownloadingFormat(null)
    }
  }


  const duration = media
    ? formatDuration(media.duration)
    : null


  return (
    <main className="page">
      <section className="hero">
        <span className="eyebrow">
          MEDIA DOWNLOADER
        </span>

        <h1>Baixe sua mídia.</h1>

        <p>
          Cole o link de um vídeo público e escolha como deseja baixar.
        </p>

        <div className="search">
          <input
            type="url"
            placeholder="Cole o link aqui..."
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleAnalyze()
              }
            }}
          />

          <button
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? "Analisando..." : "Analisar"}
          </button>
        </div>

        {error && (
          <p className="error">
            {error}
          </p>
        )}
      </section>

      {media && (
        <section className="result">
          {media.thumbnail && (
            <img
              src={media.thumbnail}
              alt={media.title || "Thumbnail"}
            />
          )}

          <div className="media-content">
            <div className="media-meta">
              {media.platform && (
                <span className="platform">
                  {media.platform}
                </span>
              )}

              {duration && (
                <span>{duration}</span>
              )}
            </div>

            <h2>{media.title}</h2>

            {media.uploader && (
              <p className="uploader">
                {media.uploader}
              </p>
            )}

            <div className="formats">
              {media.formats.map((format) => {
                const isDownloading =
                  downloadingFormat === format.format_id

                const fileSize =
                  formatFileSize(format.filesize)

                const isAudio =
                  format.type === "audio"

                return (
                  <button
                    className={`format ${
                      isAudio ? "format-audio" : ""
                    }`}
                    key={format.format_id}
                    onClick={() =>
                      handleDownload(format.format_id)
                    }
                    disabled={downloadingFormat !== null}
                  >
                    <div className="format-info">
                      <strong>
                        {isAudio
                          ? "Somente áudio"
                          : format.quality}
                      </strong>

                      <span>
                        {isAudio
                          ? `${format.quality} • ${format.ext?.toUpperCase()}`
                          : format.ext?.toUpperCase()}
                      </span>
                    </div>

                    <div className="format-action">
                      {fileSize && (
                        <span>{fileSize}</span>
                      )}

                      <strong>
                        {isDownloading
                          ? "Preparando..."
                          : "Baixar"}
                      </strong>
                    </div>
                  </button>
                )
              })}
            </div>
          </div>
        </section>
      )}
    </main>
  )
}

export default App