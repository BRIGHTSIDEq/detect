import Foundation

struct GroupingSettings { var minIoU = 0.02; var maxCenterDistanceRatio = 1.75; var maxGapRatio = 0.65; var sizeSimilarityMin = 0.25 }
final class GroupingService {
    func group(_ detections: [Detection], settings: GroupingSettings = .init()) -> [DetectionGroup] {
        var used = Set<UUID>(); var result: [DetectionGroup] = []
        for d in detections where !used.contains(d.id) {
            var bucket = [d]; used.insert(d.id)
            for o in detections where !used.contains(o.id) && shouldMerge(d, o, settings) { bucket.append(o); used.insert(o.id) }
            let union = bucket.dropFirst().reduce(d.box) { $0.union($1.box) }
            let areaSum = bucket.reduce(0.0) { $0 + max(0.000001, $1.box.width * $1.box.height) }
            let conf = bucket.reduce(0.0) { $0 + $1.confidence * max(0.000001, $1.box.width * $1.box.height) } / areaSum
            result.append(DetectionGroup(id: UUID(), classId: d.classId, className: d.className, confidence: conf, box: union, detections: bucket))
        }
        return result
    }
    private func shouldMerge(_ a: Detection, _ b: Detection, _ s: GroupingSettings) -> Bool {
        guard a.classId == b.classId else { return false }
        let size = min(a.box.area, b.box.area) / max(a.box.area, b.box.area)
        if size < s.sizeSimilarityMin { return false }
        if a.box.iou(b.box) >= s.minIoU { return true }
        let scale = (a.box.width + a.box.height + b.box.width + b.box.height) / 4
        return a.box.centerDistance(to: b.box) / scale <= s.maxCenterDistanceRatio && a.box.gap(to: b.box) / scale <= s.maxGapRatio
    }
}
extension CGRect { var area: Double { width * height }; func iou(_ o: CGRect) -> Double { let i = intersection(o); let ia = i.isNull ? 0 : i.area; let u = area + o.area - ia; return u > 0 ? ia / u : 0 }; func centerDistance(to o: CGRect) -> Double { hypot(midX-o.midX, midY-o.midY) }; func gap(to o: CGRect) -> Double { hypot(max(o.minX-maxX,minX-o.maxX,0), max(o.minY-maxY,minY-o.maxY,0)) } }
