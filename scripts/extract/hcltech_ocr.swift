// OCR image-only HCLTech investor-release pages using macOS Vision.
// Usage: swift hcltech_ocr.swift page.png  -> prints lines reconstructed by y position
import Foundation
import Vision
import AppKit

let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { exit(1) }
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try handler.perform([req])
struct Tok { var x: Double; var y: Double; var h: Double; var s: String }
var toks: [Tok] = []
for obs in req.results ?? [] {
    guard let c = obs.topCandidates(1).first else { continue }
    let b = obs.boundingBox
    toks.append(Tok(x: b.minX, y: 1 - b.midY, h: b.height, s: c.string))
}
toks.sort { $0.y < $1.y }
var rows: [[Tok]] = []
for t in toks {
    if var last = rows.last, let f = last.first, abs(f.y - t.y) < max(0.006, f.h * 0.5) {
        last.append(t); rows[rows.count - 1] = last
    } else { rows.append([t]) }
}
for r in rows {
    let s = r.sorted { $0.x < $1.x }
    var line = ""
    for t in s {
        let col = Int(t.x * 200)
        if line.count < col { line += String(repeating: " ", count: col - line.count) } else if !line.isEmpty { line += "  " }
        line += t.s
    }
    print(line)
}
