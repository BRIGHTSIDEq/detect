import Foundation
import SwiftData

struct Detection: Identifiable, Codable, Equatable { let id: UUID; let classId: Int; let className: String; let confidence: Double; let box: CGRect }
struct DetectionGroup: Identifiable, Codable, Equatable { let id: UUID; let classId: Int; let className: String; let confidence: Double; let box: CGRect; let detections: [Detection]; var count: Int { detections.count } }
@Model final class RecognitionRecord { var createdAt: Date; var source: String; var groupsJSON: String; init(createdAt: Date = .now, source: String, groupsJSON: String) { self.createdAt = createdAt; self.source = source; self.groupsJSON = groupsJSON } }
