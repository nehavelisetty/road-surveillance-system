"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { AlertTriangle, Camera, Upload, Play, Pause, BarChart3 } from "lucide-react"

interface DetectionResult {
  id: string
  timestamp: string
  type: "lane_marking" | "road_damage"
  confidence: number
  location: { x: number; y: number; width: number; height: number }
  severity?: "low" | "medium" | "high"
}

export default function RoadSurveillanceDashboard() {
  const [isProcessing, setIsProcessing] = useState(false)
  const [detections, setDetections] = useState<DetectionResult[]>([])
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [processingProgress, setProcessingProgress] = useState(0)
  const [stats, setStats] = useState({
    totalDetections: 0,
    laneMarkings: 0,
    roadDamage: 0,
    highSeverity: 0,
  })

  // Simulate real-time detection updates
  useEffect(() => {
    if (isProcessing) {
      const interval = setInterval(() => {
        const newDetection: DetectionResult = {
          id: Math.random().toString(36).substr(2, 9),
          timestamp: new Date().toISOString(),
          type: Math.random() > 0.5 ? "lane_marking" : "road_damage",
          confidence: Math.random() * 0.4 + 0.6, // 60-100%
          location: {
            x: Math.random() * 800,
            y: Math.random() * 600,
            width: Math.random() * 100 + 50,
            height: Math.random() * 100 + 50,
          },
          severity: ["low", "medium", "high"][Math.floor(Math.random() * 3)] as "low" | "medium" | "high",
        }

        setDetections((prev) => [newDetection, ...prev.slice(0, 9)])
        setProcessingProgress((prev) => Math.min(prev + Math.random() * 10, 100))

        // Update stats
        setStats((prev) => ({
          totalDetections: prev.totalDetections + 1,
          laneMarkings: prev.laneMarkings + (newDetection.type === "lane_marking" ? 1 : 0),
          roadDamage: prev.roadDamage + (newDetection.type === "road_damage" ? 1 : 0),
          highSeverity: prev.highSeverity + (newDetection.severity === "high" ? 1 : 0),
        }))
      }, 2000)

      return () => clearInterval(interval)
    }
  }, [isProcessing])

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  const startProcessing = () => {
    setIsProcessing(true)
    setProcessingProgress(0)
    setDetections([])
  }

  const stopProcessing = () => {
    setIsProcessing(false)
    setProcessingProgress(0)
  }

  const getSeverityColor = (severity?: string) => {
    switch (severity) {
      case "high":
        return "bg-red-500"
      case "medium":
        return "bg-yellow-500"
      case "low":
        return "bg-green-500"
      default:
        return "bg-gray-500"
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-gray-900">Road Surveillance System</h1>
          <p className="text-lg text-gray-600">Real-time Lane Markings and Road Damage Detection</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Detections</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalDetections}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Lane Markings</CardTitle>
              <Camera className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.laneMarkings}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Road Damage</CardTitle>
              <AlertTriangle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.roadDamage}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">High Severity</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{stats.highSeverity}</div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="live" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="live">Live Detection</TabsTrigger>
            <TabsTrigger value="upload">Upload & Process</TabsTrigger>
            <TabsTrigger value="results">Detection Results</TabsTrigger>
          </TabsList>

          <TabsContent value="live" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Live Camera Feed</CardTitle>
                <CardDescription>Real-time detection from camera input</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-black rounded-lg aspect-video flex items-center justify-center">
                  <div className="text-white text-center">
                    <Camera className="h-16 w-16 mx-auto mb-4 opacity-50" />
                    <p className="text-lg">Camera Feed Placeholder</p>
                    <p className="text-sm opacity-75">Connect camera to start live detection</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <Button onClick={startProcessing} disabled={isProcessing}>
                    <Play className="h-4 w-4 mr-2" />
                    Start Detection
                  </Button>
                  <Button onClick={stopProcessing} disabled={!isProcessing} variant="outline">
                    <Pause className="h-4 w-4 mr-2" />
                    Stop Detection
                  </Button>
                </div>
                {isProcessing && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Processing...</span>
                      <span>{Math.round(processingProgress)}%</span>
                    </div>
                    <Progress value={processingProgress} />
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="upload" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Upload Video/Image</CardTitle>
                <CardDescription>Upload media files for batch processing</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="file-upload">Select File</Label>
                  <Input id="file-upload" type="file" accept="video/*,image/*" onChange={handleFileUpload} />
                </div>
                {selectedFile && (
                  <div className="p-4 bg-gray-100 rounded-lg">
                    <p className="font-medium">{selectedFile.name}</p>
                    <p className="text-sm text-gray-600">Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                )}
                <Button onClick={startProcessing} disabled={!selectedFile || isProcessing}>
                  <Upload className="h-4 w-4 mr-2" />
                  Process File
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="results" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Detection Results</CardTitle>
                <CardDescription>Recent detections and analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {detections.length === 0 ? (
                    <p className="text-center text-gray-500 py-8">
                      No detections yet. Start processing to see results.
                    </p>
                  ) : (
                    detections.map((detection) => (
                      <div key={detection.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <Badge variant={detection.type === "road_damage" ? "destructive" : "default"}>
                              {detection.type.replace("_", " ").toUpperCase()}
                            </Badge>
                            {detection.severity && (
                              <Badge className={getSeverityColor(detection.severity)}>
                                {detection.severity.toUpperCase()}
                              </Badge>
                            )}
                          </div>
                          <p className="text-sm text-gray-600">
                            Confidence: {(detection.confidence * 100).toFixed(1)}%
                          </p>
                          <p className="text-xs text-gray-500">{new Date(detection.timestamp).toLocaleString()}</p>
                        </div>
                        <div className="text-right text-sm text-gray-600">
                          <p>
                            Location: ({Math.round(detection.location.x)}, {Math.round(detection.location.y)})
                          </p>
                          <p>
                            Size: {Math.round(detection.location.width)}×{Math.round(detection.location.height)}
                          </p>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
