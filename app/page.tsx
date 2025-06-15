'use client';

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function RoadSurveillanceDashboard() {
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);

  // ⬇️ Function to send image blob to /api/upload
  const sendToBackend = async (blob: Blob) => {
    const formData = new FormData();
    formData.append("image", blob, "road.jpg");

    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();
      console.log("Server response:", result);
    } catch (err) {
      console.error("Upload error:", err);
    }
  };

  // ⬇️ File upload handler
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
        sendToBackend(file); // Send file to backend
      };
      reader.readAsDataURL(file);
    }
  };

  // ⬇️ Start camera stream
  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (error) {
      console.error("Camera access error:", error);
    }
  };

  // ⬇️ Capture image from video and send it
  const captureImage = () => {
    const video = videoRef.current;
    if (!video) return;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    if (ctx) {
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      canvas.toBlob((blob) => {
        if (blob) {
          const imageUrl = URL.createObjectURL(blob);
          setImagePreview(imageUrl);
          sendToBackend(blob); // Send captured image to backend
        }
      }, "image/jpeg");
    }
  };

  return (
    <div className="p-4 space-y-4">
      <Label htmlFor="upload">Upload Road Image</Label>
      <Input id="upload" type="file" accept="image/*" onChange={handleFileChange} />

      <div className="mt-6">
        <Button onClick={startCamera}>Start Camera</Button>
        <video ref={videoRef} autoPlay className="mt-2 rounded border w-full max-w-md" />
        <Button className="mt-2" onClick={captureImage}>Capture Image</Button>
      </div>

      {imagePreview && (
        <div className="mt-4">
          <p className="text-sm text-muted-foreground">Image Preview:</p>
          <img src={imagePreview} alt="Preview" className="rounded border mt-2 max-w-md" />
        </div>
      )}
    </div>
  );
}
