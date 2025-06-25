import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Home, Search } from "lucide-react"
import { CricketStumps } from "@/components/cricket-icons"

export default function NotFound() {
  return (
    <div className="min-h-screen cricket-field-bg flex items-center justify-center p-4">
      <Card className="max-w-md w-full border-green-200">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <CricketStumps className="w-12 h-12 text-green-600" />
          </div>
          <CardTitle className="text-green-800">Page Not Found</CardTitle>
          <CardDescription>
            The page you're looking for doesn't exist. It might have been moved or deleted.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button asChild className="w-full bg-green-600 hover:bg-green-700">
            <Link href="/" className="flex items-center space-x-2">
              <Home className="w-4 h-4" />
              <span>Go Home</span>
            </Link>
          </Button>

          <Button asChild variant="outline" className="w-full border-green-600 text-green-600">
            <Link href="/player-stats" className="flex items-center space-x-2">
              <Search className="w-4 h-4" />
              <span>Search Player Stats</span>
            </Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
