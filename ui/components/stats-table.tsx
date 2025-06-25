import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import type { BattingStats, BowlingStats } from "@/lib/api"

interface StatsTableProps {
  stats: BattingStats | BowlingStats
  statsType: "batting" | "bowling"
}

export function StatsTable({ stats, statsType }: StatsTableProps) {
  const getStatColor = (statName: string, value: string) => {
    if (value === "0" || value === "-/-") return "text-gray-400"

    if (statsType === "batting") {
      if (statName === "100s" && Number.parseInt(value) > 0) return "text-green-600 font-semibold"
      if (statName === "50s" && Number.parseInt(value) > 10) return "text-blue-600 font-semibold"
      if (statName === "Highest" && Number.parseInt(value) > 150) return "text-purple-600 font-semibold"
    } else {
      if (statName === "5w" && Number.parseInt(value) > 0) return "text-green-600 font-semibold"
      if (statName === "Wickets" && Number.parseInt(value) > 100) return "text-blue-600 font-semibold"
    }

    return "text-gray-900"
  }

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
    <Card className="border-green-200">
      <CardHeader>
        <CardTitle className="text-green-800">
          Detailed {statsType === "batting" ? "Batting" : "Bowling"} Statistics
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="font-semibold text-green-800">Statistic</TableHead>
                {stats.headers.slice(1).map((header) => (
                  <TableHead key={header} className="text-center">
                    <Badge variant="outline" className={getFormatBadgeColor(header)}>
                      {header}
                    </Badge>
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {stats.values.map((row, index) => (
                <TableRow key={index} className="hover:bg-green-50">
                  <TableCell className="font-medium text-green-700">{row.values[0]}</TableCell>
                  {row.values.slice(1).map((value, valueIndex) => (
                    <TableCell key={valueIndex} className={`text-center ${getStatColor(row.values[0], value)}`}>
                      {value}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  )
}
