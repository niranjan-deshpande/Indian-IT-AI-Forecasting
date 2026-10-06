// OCR an image with macOS Vision; prints one JSON object per recognized text box: y (top=0), x0, x1, h, text
import Foundation
import Vision
import AppKit
let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("ERR load"); exit(1) }
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
let h = VNImageRequestHandler(cgImage: cg, options: [:])
try h.perform([req])
for o in req.results ?? [] { if let t = o.topCandidates(1).first {
  let b = o.boundingBox
  let d: [String: Any] = ["y": 1 - Double(b.midY), "x0": Double(b.minX), "x1": Double(b.maxX), "h": Double(b.height), "t": t.string]
  let j = try JSONSerialization.data(withJSONObject: d); print(String(data: j, encoding: .utf8)!) } }
