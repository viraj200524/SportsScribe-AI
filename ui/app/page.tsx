import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, BarChart3, Download, Zap } from "lucide-react"
import { CricketBat, CricketBall, CricketStumps } from "@/components/cricket-icons"

export default function HomePage() {
  return (
    <div className="min-h-screen cricket-field-bg">
      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <div className="flex justify-center mb-6">
            <div className="relative">
              <CricketBall className="w-16 h-16 text-red-500 animate-bounce" />
              <CricketBat className="w-12 h-12 text-amber-600 absolute -right-4 -bottom-2 rotate-45" />
            </div>
          </div>

          <h1 className="text-5xl font-bold text-green-800 mb-6">Cricket Journalism Automation</h1>

          <p className="text-xl text-green-700 mb-8 max-w-3xl mx-auto">
            Revolutionize sports journalism with AI-powered report generation and comprehensive cricket statistics
            analysis. Generate professional reports and analyze player performance across all formats.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg" className="bg-green-600 hover:bg-green-700">
              <Link href="/report-generator" className="flex items-center space-x-2">
                <FileText className="w-5 h-5" />
                <span>Generate Reports</span>
              </Link>
            </Button>

          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-green-800 mb-12">
            Powerful Features for Cricket Journalism
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="border-green-200 hover:shadow-lg transition-shadow">
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                    <Zap className="w-6 h-6 text-green-600" />
                  </div>
                </div>
                <CardTitle className="text-green-800">AI-Powered Reports</CardTitle>
                <CardDescription>
                  Generate comprehensive match reports and analysis using advanced AI technology
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• Instant report generation</li>
                  <li>• Professional formatting</li>
                  <li>• Match analysis and insights</li>
                  <li>• Downloadable DOCX format</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-green-200 hover:shadow-lg transition-shadow">
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                    <BarChart3 className="w-6 h-6 text-red-600" />
                  </div>
                </div>
                <CardTitle className="text-green-800">Sporty Narrative Voiceover</CardTitle>
                <CardDescription>
                  High-energy, commentary-style voiceover for cricket match reports.
                </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li>• Converts reports into dynamic, match-like narration</li>
                    <li>• Adds excitement to Test, ODI, T20, and IPL updates</li>
                    <li>• Perfect for podcasts, reels, and automated voiceovers</li>
                    <li>• Highlights turning points and player performances</li>
                  </ul>
                </CardContent>

            </Card>

            <Card className="border-green-200 hover:shadow-lg transition-shadow">
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center">
                    <Download className="w-6 h-6 text-amber-600" />
                  </div>
                </div>
                <CardTitle className="text-green-800">Export & Share</CardTitle>
                <CardDescription>Export reports and statistics in multiple formats for easy sharing</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• DOCX report downloads</li>
                  <li>• Professional formatting</li>
                  <li>• Ready for publication</li>
                  <li>• Audio Report Download</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4">
        <div className="container mx-auto text-center">
          <div className="flex justify-center mb-6">
            <CricketStumps className="w-12 h-12 text-green-600" />
          </div>

          <h2 className="text-3xl font-bold text-green-800 mb-4">Ready to Transform Your Cricket Journalism?</h2>

          <p className="text-lg text-green-700 mb-8 max-w-2xl mx-auto">
            Join the future of sports journalism with our AI-powered platform. Generate professional reports and analyze
            player statistics in seconds.
          </p>

          <Button asChild size="lg" className="bg-red-600 hover:bg-red-700">
            <Link href="/report-generator" className="flex items-center space-x-2">
              <CricketBall className="w-5 h-5" />
              <span>Start Generating Reports</span>
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
