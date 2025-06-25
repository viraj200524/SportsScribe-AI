import { Loader2 } from "lucide-react"
import { CricketBall } from "@/components/cricket-icons"

export default function Loading() {
  return (
    <div className="min-h-screen cricket-field-bg flex items-center justify-center">
      <div className="text-center">
        <div className="relative mb-6">
          <CricketBall className="w-16 h-16 text-red-500 animate-bounce mx-auto" />
          <Loader2 className="w-8 h-8 text-green-600 animate-spin absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
        </div>
        <h2 className="text-2xl font-bold text-green-800 mb-2">Loading Cricket Data</h2>
        <p className="text-green-700">Please wait while we fetch the latest information...</p>
      </div>
    </div>
  )
}
