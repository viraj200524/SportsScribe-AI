"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, FileText, Download, AlertCircle, CheckCircle, Mic, MicOff, Volume2, Play, Pause, VolumeX } from "lucide-react"
import { CricketBall } from "@/components/cricket-icons"
import { generateReport, downloadReport } from "@/lib/api"
import ReactMarkdown from "react-markdown"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism"
import remarkGfm from "remark-gfm"

// Function to extract Markdown content from HTML
const extractMarkdownFromHtml = (html: string): string => {
  // Use regex to find content within <code class="language-markdown">...</code>
  const markdownRegex = /<code class="language-markdown">([\s\S]*?)<\/code>/
  const match = html.match(markdownRegex)
  // Decode HTML entities (e.g., &lt; to <) and return the content or fallback to empty string
  if (match && match[1]) {
    return match[1].replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&")
  }
  return ""
}

export default function ReportGeneratorPage() {
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [markdownContent, setMarkdownContent] = useState(``)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  
  // Audio narration states
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false)
  const [audioUrl, setAudioUrl] = useState("")
  const [audioError, setAudioError] = useState("")
  const [audioFilename, setAudioFilename] = useState("")
  const [isPlaying, setIsPlaying] = useState(false)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  
  // Speech recognition states
  const [isListening, setIsListening] = useState(false)
  const [speechSupported, setSpeechSupported] = useState(false)
  const [speechError, setSpeechError] = useState("")
  const recognitionRef = useRef<any>(null)
  const silenceTimerRef = useRef<NodeJS.Timeout | null>(null)

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
      if (SpeechRecognition) {
        setSpeechSupported(true)
        recognitionRef.current = new SpeechRecognition()
        recognitionRef.current.continuous = true
        recognitionRef.current.interimResults = true
        recognitionRef.current.lang = 'en-US'

        recognitionRef.current.onresult = (event: any) => {
          let finalTranscript = ''
          let interimTranscript = ''

          // Reset silence timer on new speech
          if (silenceTimerRef.current) {
            clearTimeout(silenceTimerRef.current)
          }

          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript
            if (event.results[i].isFinal) {
              finalTranscript += transcript
            } else {
              interimTranscript += transcript
            }
          }

          if (finalTranscript) {
            setInput(prev => prev + finalTranscript + ' ')
          }

          // Start silence timer after processing speech
          silenceTimerRef.current = setTimeout(() => {
            if (isListening) {
              stopListening()
            }
          }, 3000) // 3 seconds of silence
        }

        recognitionRef.current.onerror = (event: any) => {
          setSpeechError(`Speech recognition error: ${event.error}`)
          setIsListening(false)
        }

        recognitionRef.current.onend = () => {
          setIsListening(false)
          if (silenceTimerRef.current) {
            clearTimeout(silenceTimerRef.current)
          }
        }
      }
    }
  }, [])

  const startListening = () => {
    if (recognitionRef.current && speechSupported) {
      setSpeechError("")
      setIsListening(true)
      recognitionRef.current.start()
    }
  }

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop()
      setIsListening(false)
      if (silenceTimerRef.current) {
        clearTimeout(silenceTimerRef.current)
      }
    }
  }

  const clearInput = () => {
    setInput("")
    setSpeechError("")
  }

  const handleGenerateReport = async () => {
    if (!input.trim()) {
      setError("Please enter a query to generate a report.")
      return
    }

    setIsLoading(true)
    setError("")
    setSuccess("")
    setMarkdownContent("")

    try {
      const html = await generateReport(input)
      const markdown = extractMarkdownFromHtml(html)
      if (!markdown) {
        throw new Error("No valid Markdown content found in the response.")
      }
      setMarkdownContent(markdown)
      setSuccess("Report generated successfully! You can now preview and download it.")
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An unexpected error occurred"
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const handleGenerateAudio = async () => {
    if (!markdownContent.trim()) {
      setAudioError("No content available to generate narration.")
      return
    }

    setIsGeneratingAudio(true)
    setAudioError("")
    setAudioUrl("")

    try {
      const response = await fetch('http://127.0.0.1:8000/generate-narration-audio', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: markdownContent }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      console.log('Audio response:', data) // Debug log
      
      // Construct full URL if needed
      const fullAudioUrl = data.audio_url

      console.log('Full audio URL:', fullAudioUrl) // Debug log
      
      setAudioUrl(fullAudioUrl)
      setAudioFilename(data.filename)
      setSuccess("Audio narration generated successfully!")
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to generate audio narration"
      setAudioError(errorMessage)
    } finally {
      setIsGeneratingAudio(false)
    }
  }

  useEffect(() => {
  if (audioRef.current && audioUrl) {
    audioRef.current.load()
  }
}, [audioUrl])


  const handlePlayPause = () => {
  if (!audioRef.current || !audioUrl) {
    setAudioError("Audio not available")
    return
  }

  // Only try to play if src is set and audio can be loaded
  if (isPlaying) {
    audioRef.current.pause()
    setIsPlaying(false)
  } else {
    audioRef.current.play().then(() => {
      setIsPlaying(true)
    }).catch(error => {
      setAudioError(`Failed to play audio: ${error.message}`)
      setIsPlaying(false)
    })
  }
}


  const handleDownloadAudio = async () => {
    if (!audioFilename) return

    try {
      const response = await fetch(`http://127.0.0.1:8000/audio/${audioFilename}`)
      if (!response.ok) throw new Error('Download failed')
      
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = audioFilename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      setSuccess("Audio file downloaded successfully!")
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to download audio"
      setAudioError(errorMessage)
    }
  }

  const handleDownloadReport = async () => {
    try {
      await downloadReport()
      setSuccess("Download started successfully!")
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to download report"
      setError(errorMessage)
    }
  }

  return (
    <div className="min-h-screen cricket-field-bg py-8 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <CricketBall className="w-12 h-12 text-red-500" />
          </div>
          <h1 className="text-4xl font-bold text-green-800 mb-2">Cricket Report Generator</h1>
          <p className="text-lg text-green-700">Generate professional cricket reports using AI-powered analysis</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <Card className="border-green-200">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2 text-green-800">
                <FileText className="w-5 h-5" />
                <span>Report Query</span>
              </CardTitle>
              <CardDescription>
                Enter details about the match, series, or cricket topic you want to generate a report for. You can type or use voice input.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="relative">
                <Textarea
                  placeholder="Example: Generate a report for the recent India vs Australia Test match at Melbourne Cricket Ground, focusing on batting performances and key moments..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  rows={6}
                  className="resize-none"
                />
              </div>

              {/* Speech Status */}
              {speechSupported && isListening && (
                <Alert className="border-blue-200 bg-blue-50">
                  <Volume2 className="h-4 w-4 text-blue-600 animate-pulse" />
                  <AlertDescription className="text-blue-800">
                    Listening... Speak your query now
                  </AlertDescription>
                </Alert>
              )}

              {speechError && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{speechError}</AlertDescription>
                </Alert>
              )}

              {!speechSupported && (
                <Alert className="border-orange-200 bg-orange-50">
                  <AlertCircle className="h-4 w-4 text-orange-600" />
                  <AlertDescription className="text-orange-800">
                    Speech recognition is not supported in your browser. Please type your query.
                  </AlertDescription>
                </Alert>
              )}

              <div className="flex gap-2">
                <Button
                  onClick={handleGenerateReport}
                  disabled={isLoading || !input.trim()}
                  className="flex-1 bg-green-600 hover:bg-green-700"
                  size="lg"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Generating Report...
                    </>
                  ) : (
                    <>
                      <CricketBall className="w-4 h-4 mr-2" />
                      Generate Report
                    </>
                  )}
                </Button>

                {speechSupported && (
                  <Button
                    onClick={isListening ? stopListening : startListening}
                    disabled={isLoading}
                    variant={isListening ? "destructive" : "default"}
                    className={isListening ? 
                      "bg-red-600 hover:bg-red-700 text-white" : 
                      "bg-blue-600 hover:bg-blue-700 text-white"
                    }
                    size="lg"
                    title={isListening ? "Stop listening" : "Start voice input"}
                  >
                    {isListening ? (
                      <MicOff className="w-4 h-4" />
                    ) : (
                      <Mic className="w-4 h-4" />
                    )}
                  </Button>
                )}
              </div>

              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {success && (
                <Alert className="border-green-200 bg-green-50">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <AlertDescription className="text-green-800">{success}</AlertDescription>
                </Alert>
              )}

              {markdownContent && (
                <Button
                  onClick={handleDownloadReport}
                  variant="outline"
                  className="w-full border-green-600 text-green-600 hover:bg-green-50"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Download Report (DOCX)
                </Button>
              )}
            </CardContent>
          </Card>

          {/* Preview Section */}
          <Card className="border-green-200">
            <CardHeader>
              <CardTitle className="text-green-800">Report Preview</CardTitle>
              <CardDescription>Generated report will appear here in Markdown format</CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <Loader2 className="w-8 h-8 animate-spin text-green-600 mx-auto mb-4" />
                    <p className="text-green-700">Generating your cricket report...</p>
                  </div>
                </div>
              ) : markdownContent ? (
                <div className="space-y-4">
                  <div className="report-preview bg-white rounded-lg p-6 border border-green-200 max-h-96 overflow-y-auto">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        code({ node, inline, className, children, ...props }) {
                          const match = /language-(\w+)/.exec(className || "")
                          return !inline && match ? (
                            <SyntaxHighlighter
                              style={vscDarkPlus}
                              language={match[1]}
                              PreTag="div"
                              {...props}
                            >
                              {String(children).replace(/\n$/, "")}
                            </SyntaxHighlighter>
                          ) : (
                            <code className={className} {...props}>
                              {children}
                            </code>
                          )
                        },
                      }}
                    >
                      {markdownContent}
                    </ReactMarkdown>
                  </div>

                  {/* Audio Narration Section */}
                  <div className="space-y-3">
                    <Button
                      onClick={handleGenerateAudio}
                      disabled={isGeneratingAudio}
                      className="w-full bg-purple-600 hover:bg-purple-700"
                      size="sm"
                    >
                      {isGeneratingAudio ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          Generating Audio...
                        </>
                      ) : (
                        <>
                          <Volume2 className="w-4 h-4 mr-2" />
                          Hear the Report
                        </>
                      )}
                    </Button>

                    {audioError && (
                      <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertDescription>{audioError}</AlertDescription>
                      </Alert>
                    )}

                    {audioUrl && (
                      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-sm font-medium text-gray-700">Audio Narration</span>
                          <Button
                            onClick={handleDownloadAudio}
                            variant="outline"
                            size="sm"
                            className="border-gray-300 text-gray-600 hover:bg-gray-100"
                          >
                            <Download className="w-3 h-3 mr-1" />
                            Download
                          </Button>
                        </div>
                        
                        <div className="flex items-center space-x-3">
                          <Button
                            onClick={handlePlayPause}
                            variant="outline"
                            size="sm"
                            className="border-purple-600 text-purple-600 hover:bg-purple-50"
                          >
                            {isPlaying ? (
                              <Pause className="w-4 h-4" />
                            ) : (
                              <Play className="w-4 h-4" />
                            )}
                          </Button>
                          
                          <div className="flex-1">
                            <audio
                              ref={audioRef}
                              src={"http://localhost:8000"+audioUrl || undefined}
                              className="w-full"
                              controls
                              onPlay={() => setIsPlaying(true)}
                              onPause={() => setIsPlaying(false)}
                              onEnded={() => setIsPlaying(false)}
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>Your generated report will appear here</p>
                  <p className="text-sm mt-2">Enter a query and click "Generate Report" to get started</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Usage Instructions */}
        <Card className="mt-8 border-blue-200">
          <CardHeader>
            <CardTitle className="text-blue-800 flex items-center space-x-2">
              <Volume2 className="w-5 h-5" />
              <span>Voice Input Instructions</span>
            </CardTitle>
            <CardDescription>How to use the speech-to-text feature effectively</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <h4 className="font-semibold text-blue-700">Getting Started</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Click the microphone icon to start voice input</li>
                  <li>• Speak clearly and at a normal pace</li>
                  <li>• The system will automatically transcribe your speech</li>
                  <li>• Click the microphone again to stop listening</li>
                </ul>
              </div>
              <div className="space-y-2">
                <h4 className="font-semibold text-blue-700">Tips for Better Results</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Use clear pronunciation for cricket terms</li>
                  <li>• Pause between different topics or sections</li>
                  <li>• You can edit the transcribed text before generating</li>
                  <li>• Combine voice input with typing for best results</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Example Queries */}
        <Card className="mt-8 border-green-200">
          <CardHeader>
            <CardTitle className="text-green-800">Example Queries</CardTitle>
            <CardDescription>Try these sample queries to get started with report generation</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <h4 className="font-semibold text-green-700">Match Reports</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• "Generate a report for India vs England ODI series"</li>
                  <li>• "Analyze the recent IPL final match performance"</li>
                  <li>• "Create a summary of the Ashes Test series"</li>
                </ul>
              </div>
              <div className="space-y-2">
                <h4 className="font-semibold text-green-700">Player Analysis</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• "Report on Virat Kohli's recent batting form"</li>
                  <li>• "Analyze Jasprit Bumrah's bowling statistics"</li>
                  <li>• "Compare top batsmen in current IPL season"</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}