import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Trophy, Target, Zap, Award } from "lucide-react"
import type { BattingStats, BowlingStats } from "@/lib/api"

interface StatsCardsProps {
  stats: BattingStats | BowlingStats
  statsType: "batting" | "bowling"
}

export function StatsCards({ stats, statsType }: StatsCardsProps) {
  const getKeyStats = () => {
    if (statsType === "batting") {
      const runsRow = stats.values.find((row) => row.values[0] === "Runs")
      const averageRow = stats.values.find((row) => row.values[0] === "Average")
      const hundredsRow = stats.values.find((row) => row.values[0] === "100s")
      const highestRow = stats.values.find((row) => row.values[0] === "Highest")

      return [
        {
          title: "Total Runs",
          icon: Trophy,
          stats: runsRow ? runsRow.values.slice(1) : [],
          color: "text-green-600",
        },
        {
          title: "Average",
          icon: Target,
          stats: averageRow ? averageRow.values.slice(1) : [],
          color: "text-blue-600",
        },
        {
          title: "Centuries",
          icon: Award,
          stats: hundredsRow ? hundredsRow.values.slice(1) : [],
          color: "text-purple-600",
        },
        {
          title: "Highest Score",
          icon: Zap,
          stats: highestRow ? highestRow.values.slice(1) : [],
          color: "text-red-600",
        },
      ]
    } else {
      const wicketsRow = stats.values.find((row) => row.values[0] === "Wickets")
      const averageRow = stats.values.find((row) => row.values[0] === "Avg")
      const economyRow = stats.values.find((row) => row.values[0] === "Eco")
      const fiveWicketsRow = stats.values.find((row) => row.values[0] === "5w")

      return [
        {
          title: "Total Wickets",
          icon: Trophy,
          stats: wicketsRow ? wicketsRow.values.slice(1) : [],
          color: "text-green-600",
        },
        {
          title: "Bowling Average",
          icon: Target,
          stats: averageRow ? averageRow.values.slice(1) : [],
          color: "text-blue-600",
        },
        {
          title: "Economy Rate",
          icon: Zap,
          stats: economyRow ? economyRow.values.slice(1) : [],
          color: "text-orange-600",
        },
        {
          title: "5-Wicket Hauls",
          icon: Award,
          stats: fiveWicketsRow ? fiveWicketsRow.values.slice(1) : [],
          color: "text-purple-600",
        },
      ]
    }
  }

  const keyStats = getKeyStats()
  const formats = stats.headers.slice(1)

  const getFormatBadgeColor = (format: string) => {
    switch (format) {
      case "Test":
        return "bg-red-100 text-red-800"
      case "ODI":
        return "bg-blue-100 text-blue-800"
      case "T20":
        return "bg-green-100 text-green-800"
      case "IPL":
        return "bg-purple-100 text-purple-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {keyStats.map((stat, index) => {
        const Icon = stat.icon
        return (
          <Card key={index} className="border-green-200 hover:shadow-md transition-shadow">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center space-x-2 text-sm">
                <Icon className={`w-4 h-4 ${stat.color}`} />
                <span className="text-green-800">{stat.title}</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {formats.map((format, formatIndex) => (
                <div key={format} className="flex items-center justify-between">
                  <Badge variant="outline" className={`text-xs ${getFormatBadgeColor(format)}`}>
                    {format}
                  </Badge>
                  <span className={`font-semibold ${stat.color}`}>{stat.stats[formatIndex] || "0"}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
