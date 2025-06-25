"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, BarChart3, AlertCircle, ExternalLink, CheckCircle } from "lucide-react"
import { CricketBat, CricketBall } from "@/components/cricket-icons"
import { getBattingStats, getBowlingStats, type BattingStats, type BowlingStats } from "@/lib/api"
import { StatsTable } from "@/components/stats-table"
import { StatsCards } from "@/components/stats-cards"

type StatsType = "batting" | "bowling"

export default function PlayerStatsPage() {
  const [playerName, setPlayerName] = useState("")
  const [statsType, setStatsType] = useState<StatsType>("batting")
  const [isLoading, setIsLoading] = useState(false)
  const [battingStats, setBattingStats] = useState<BattingStats | null>(null)
  const [bowlingStats, setBowlingStats] = useState<BowlingStats | null>(null)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  const handleFetchStats = async () => {
    if (!playerName.trim()) {
      setError("Please enter a player name.")
      return
    }

    setIsLoading(true)
    setError("")
    setSuccess("")
    setBattingStats(null)
    setBowlingStats(null)

    try {
      if (statsType === "batting") {
        const stats = await getBattingStats(playerName)
        setBattingStats(stats)
      } else {
        const stats = await getBowlingStats(playerName)
        setBowlingStats(stats)
      }

      setSuccess(`${statsType} statistics for ${playerName} have been loaded successfully.`)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An unexpected error occurred"
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const currentStats = statsType === "batting" ? battingStats : bowlingStats
  const hasStats = currentStats !== null

  return (
    <div className="min-h-screen cricket-field-bg py-8 px-4">
      <div className="container mx-auto max-w-7xl">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="relative">
              <CricketBat className="w-10 h-10 text-amber-600" />
              <CricketBall className="w-6 h-6 text-red-500 absolute -right-2 -top-1" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-green-800 mb-2">Player Statistics Dashboard</h1>
          <p className="text-lg text-green-700">Comprehensive cricket statistics across all formats</p>
        </div>

        {/* Search Form */}
        <Card className="mb-8 border-green-200">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-green-800">
              <BarChart3 className="w-5 h-5" />
              <span>Player Search</span>
            </CardTitle>
            <CardDescription>Enter a player name and select the type of statistics you want to view</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <Input
                  placeholder="Enter player name (e.g., KL Rahul, Virat Kohli)"
                  value={playerName}
                  onChange={(e) => setPlayerName(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleFetchStats()}
                />
              </div>

              <Select value={statsType} onValueChange={(value: StatsType) => setStatsType(value)}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="batting">
                    <div className="flex items-center space-x-2">
                      <CricketBat className="w-4 h-4" />
                      <span>Batting Stats</span>
                    </div>
                  </SelectItem>
                  <SelectItem value="bowling">
                    <div className="flex items-center space-x-2">
                      <CricketBall className="w-4 h-4" />
                      <span>Bowling Stats</span>
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>

              <Button
                onClick={handleFetchStats}
                disabled={isLoading || !playerName.trim()}
                className="bg-green-600 hover:bg-green-700"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Fetching...
                  </>
                ) : (
                  <>
                    {statsType === "batting" ? (
                      <CricketBat className="w-4 h-4 mr-2" />
                    ) : (
                      <CricketBall className="w-4 h-4 mr-2" />
                    )}
                    Fetch Stats
                  </>
                )}
              </Button>
            </div>

            {error && (
              <Alert variant="destructive" className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {success && (
              <Alert className="mt-4 border-green-200 bg-green-50">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <AlertDescription className="text-green-800">{success}</AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Loading State */}
        {isLoading && (
          <Card className="border-green-200">
            <CardContent className="py-12">
              <div className="text-center">
                <Loader2 className="w-8 h-8 animate-spin text-green-600 mx-auto mb-4" />
                <p className="text-green-700">
                  Fetching {statsType} statistics for {playerName}...
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Stats Display */}
        {hasStats && currentStats && (
          <div className="space-y-6">
            {/* Player Profile Card */}
            <Card className="border-green-200">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-2xl text-green-800">
                      {playerName} - {statsType === "batting" ? "Batting" : "Bowling"} Statistics
                    </CardTitle>
                    <CardDescription className="text-base">
                      Career statistics across Test, ODI, T20, and IPL formats
                    </CardDescription>
                  </div>
                  {currentStats.appIndex?.webURL && (
                    <Button variant="outline" asChild className="border-green-600 text-green-600">
                      <a
                        href={currentStats.appIndex.webURL}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center space-x-2"
                      >
                        <ExternalLink className="w-4 h-4" />
                        <span>View on Cricbuzz</span>
                      </a>
                    </Button>
                  )}
                </div>
              </CardHeader>
            </Card>

            {/* Key Stats Cards */}
            <StatsCards stats={currentStats} statsType={statsType} />

            {/* Detailed Stats Table */}
            <StatsTable stats={currentStats} statsType={statsType} />
          </div>
        )}

        {/* Empty State */}
        {!isLoading && !hasStats && (
          <Card className="border-green-200">
            <CardContent className="py-12">
              <div className="text-center text-gray-500">
                <BarChart3 className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <h3 className="text-lg font-semibold mb-2">No Statistics Loaded</h3>
                <p>Enter a player name and click "Fetch Stats" to view detailed statistics</p>
                <div className="mt-4 text-sm">
                  <p className="font-medium mb-2">Try searching for:</p>
                  <div className="flex flex-wrap justify-center gap-2">
                    {["KL Rahul", "Virat Kohli", "Rohit Sharma", "Jasprit Bumrah"].map((name) => (
                      <Button
                        key={name}
                        variant="outline"
                        size="sm"
                        onClick={() => setPlayerName(name)}
                        className="text-xs"
                      >
                        {name}
                      </Button>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
