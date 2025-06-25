// API base URL
const API_BASE_URL = "http://127.0.0.1:8000"

// TypeScript interfaces based on the provided JSON structures
export interface StatValue {
  values: string[]
}

export interface AppIndex {
  seoTitle: string
  webURL: string
}

export interface SeriesSpinner {
  seriesId?: number
  seriesName: string
}

export interface BattingStats {
  headers: string[]
  values: StatValue[]
  appIndex: AppIndex
  seriesSpinner: SeriesSpinner[]
}

export interface BowlingStats {
  headers: string[]
  values: StatValue[]
  appIndex: AppIndex
  seriesSpinner: SeriesSpinner[]
}

// Helper function to make API calls with proper error handling
async function makeAPICall(endpoint: string, data: any, method = "POST") {
  try {
    const config: RequestInit = {
      method,
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      mode: "cors",
    }

    if (method === "POST" && data) {
      config.body = JSON.stringify(data)
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config)

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`HTTP ${response.status}: ${errorText}`)
    }

    return response
  } catch (error) {
    if (error instanceof TypeError && error.message.includes("fetch")) {
      throw new Error(
        "Unable to connect to the server. Please ensure the FastAPI server is running on http://127.0.0.1:8000",
      )
    }
    throw error
  }
}

// API call functions
export async function generateReport(input: string): Promise<string> {
  try {
    const response = await makeAPICall("/get_report", { input })
    const htmlContent = await response.text()
    return htmlContent
  } catch (error) {
    console.error("Error generating report:", error)
    const errorMessage = error instanceof Error ? error.message : "An unexpected error occurred"
    throw new Error(`Failed to generate report: ${errorMessage}`)
  }
}

export async function getBattingStats(input: string): Promise<BattingStats> {
  try {
    const response = await makeAPICall("/get_batting", { input })
    const data = await response.json()

    if (data.error) {
      throw new Error(data.error)
    }

    return data as BattingStats
  } catch (error) {
    console.error("Error fetching batting stats:", error)
    const errorMessage = error instanceof Error ? error.message : "An unexpected error occurred"
    throw new Error(`Failed to fetch batting statistics: ${errorMessage}`)
  }
}

export async function getBowlingStats(input: string): Promise<BowlingStats> {
  try {
    const response = await makeAPICall("/get_bowling", { input })
    const data = await response.json()

    if (data.error) {
      throw new Error(data.error)
    }

    return data as BowlingStats
  } catch (error) {
    console.error("Error fetching bowling stats:", error)
    const errorMessage = error instanceof Error ? error.message : "An unexpected error occurred"
    throw new Error(`Failed to fetch bowling statistics: ${errorMessage}`)
  }
}

export async function downloadReport(): Promise<void> {
  try {
    const response = await makeAPICall('/download-docx', null, "GET")

    const blob = await response.blob()

    // Extract filename from Content-Disposition header
    const disposition = response.headers.get("Content-Disposition")
    const match = disposition?.match(/filename="?([^"]+)"?/)
    const filename = match?.[1] || "report.docx"

    const url = window.URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = filename

    document.body.appendChild(link)
    link.click()

    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error("Error downloading report:", error)
    const errorMessage = error instanceof Error ? error.message : "An unexpected error occurred"
    throw new Error(`Failed to download report: ${errorMessage}`)
  }
}
