import { useState } from "react"

import "./App.css"
import { getMediaInfo } from "./services/mediaApi"
import type { MediaInfo } from "./types/media"


function App() {
  const [url, setUrl] = useState("")
  const [media, setMedia] = useState<MediaInfo | null>(null)
  const [loading, setLoading] = useState(false)
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

  return (
    <main className="page">
      <section className="hero">
        <span className="eyebrow">MEDIA DOWNLOADER</span>

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
          <p className="error">{error}</p>
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
            <span className="platform">
              {media.platform}
            </span>

            <h2>{media.title}</h2>

            {media.uploader && (
              <p>{media.uploader}</p>
            )}

            <div className="formats">
              {media.formats.map((format) => (
                <div
                  className="format"
                  key={format.format_id}
                >
                  <div>
                    <strong>{format.quality}</strong>

                    <span>
                      {format.ext?.toUpperCase()}
                    </span>
                  </div>

                  <span>
                    {format.type === "audio"
                      ? "Áudio"
                      : format.has_audio
                        ? "Vídeo + áudio"
                        : "Vídeo"}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </main>
  )
}

export default App