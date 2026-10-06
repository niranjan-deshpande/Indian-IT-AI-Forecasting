// OCR helper for image-only Tech Mahindra PDFs (macOS Vision framework, no external deps).
// Usage: swift techm_ocr.swift <page.png> [more.png ...]
// Prints recognized text lines, grouped into visual rows (left-to-right), one row per line,
// cells separated by " | ". Produced data/sources/techm/ocr/*.ocr.txt via:
//   swiftc -O -o techm_ocr techm_ocr.swift
//   pdftoppm -r 300 -png -f 1 -l 3 <file>.pdf p && ./techm_ocr p-*.png > ocr/<file>.ocr.txt
// OCR output was only used as an aid; values were visually verified before hand-entry (techm_handentered.py).
import Foundation
import Vision
import AppKit

func ocr(_ path: String) {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("ERR cannot load \(path)"); return
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    let h = VNImageRequestHandler(cgImage: cg, options: [:])
    try? h.perform([req])
    guard let obs = req.results else { return }
    // (midY, minX, text, height)
    var items: [(Double, Double, String, Double)] = []
    for o in obs {
        guard let t = o.topCandidates(1).first?.string else { continue }
        let b = o.boundingBox
        items.append((Double(1 - b.midY), Double(b.minX), t, Double(b.height)))
    }
    items.sort { $0.0 < $1.0 }
    var rows: [[(Double, Double, String, Double)]] = []
    for it in items {
        if var last = rows.last, let ref = last.first, abs(ref.0 - it.0) < max(ref.3, it.3) * 0.5 {
            last.append(it); rows[rows.count - 1] = last
        } else {
            rows.append([it])
        }
    }
    print("=== PAGE \(path)")
    for r in rows {
        let s = r.sorted { $0.1 < $1.1 }.map { $0.2 }.joined(separator: " | ")
        print(s)
    }
}

for p in CommandLine.arguments.dropFirst() { ocr(p) }
