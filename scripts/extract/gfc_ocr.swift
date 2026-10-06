// OCR an image with macOS Vision; prints recognized lines sorted top-to-bottom with x positions.
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
var items: [(Double, Double, String)] = []
for o in req.results ?? [] { if let t = o.topCandidates(1).first { items.append((1 - Double(o.boundingBox.midY), Double(o.boundingBox.minX), t.string)) } }
// group into rows by y
items.sort { $0.0 < $1.0 }
var rows: [[(Double, Double, String)]] = []
for it in items { if let last = rows.last, abs(last[0].0 - it.0) < 0.006 { rows[rows.count-1].append(it) } else { rows.append([it]) } }
for r in rows { print(r.sorted { $0.1 < $1.1 }.map { $0.2 }.joined(separator: " | ")) }
