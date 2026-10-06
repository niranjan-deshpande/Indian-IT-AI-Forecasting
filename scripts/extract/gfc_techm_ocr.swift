// OCR a PNG with macOS Vision; prints one line per recognized text box: x0 y0 x1 y1 <tab> text
// (coordinates in pixels, origin top-left). Usage: swift gfc_techm_ocr.swift image.png
import Foundation
import Vision
import AppKit
let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { exit(1) }
let W = Double(cg.width), H = Double(cg.height)
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try handler.perform([req])
for obs in req.results ?? [] {
    guard let c = obs.topCandidates(1).first else { continue }
    let b = obs.boundingBox
    let x0 = b.minX * W, x1 = b.maxX * W, y0 = (1 - b.maxY) * H, y1 = (1 - b.minY) * H
    print(String(format: "%.0f %.0f %.0f %.0f\t%@", x0, y0, x1, y1, c.string))
}
