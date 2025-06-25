"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, FileText, Download, AlertCircle, CheckCircle } from "lucide-react"
import { CricketBall } from "@/components/cricket-icons"
import { generateReport, downloadReport } from "@/lib/api"
import ReactMarkdown from "react-markdown"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism"

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
  const [markdownContent, setMarkdownContent] = useState("")
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

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
                Enter details about the match, series, or cricket topic you want to generate a report for.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Example: Generate a report for the recent India vs Australia Test match at Melbourne Cricket Ground, focusing on batting performances and key moments..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={6}
                className="resize-none"
              />

              <Button
                onClick={handleGenerateReport}
                disabled={isLoading || !input.trim()}
                className="w-full bg-green-600 hover:bg-green-700"
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
                <div className="report-preview bg-white rounded-lg p-6 border border-green-200 max-h-96 overflow-y-auto">
                  <ReactMarkdown
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