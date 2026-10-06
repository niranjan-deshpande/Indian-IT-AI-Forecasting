// OCR helper for image-only TCS GFC-window PDFs (macOS Vision framework, no external deps).
// Usage: swift gfc_tcs_ocr.swift <page.png> [more.png ...]
// Prints recognized text lines, grouped into visual rows (left-to-right), one row per line,
// cells separated by " | ". Produced data/sources/gfc/tcs/ocr/*.ocr.txt via:
//   swiftc -O -o gfc_tcs_ocr gfc_tcs_ocr.swift
//   for every page of TCS_Analysts_*.pdf whose pdftotext output has <120 non-space chars (image-only slide):
//   pdftoppm -r 200 -png -f N -l N <file>.pdf p && ./gfc_tcs_ocr p*.png >> ocr/<file>.ocr.txt  (prefixed '### PAGE N')
// OCR text is parsed by gfc_tcs_extract.py (rows flagged '[OCR of image slide]' in source_loc); USD revenue
// values were cross-checked against press-release figures and spot-checked visually against the slide images.
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
