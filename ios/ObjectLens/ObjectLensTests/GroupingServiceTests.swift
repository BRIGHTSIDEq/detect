import XCTest
@testable import ObjectLens
final class GroupingServiceTests: XCTestCase {
    func testNearApplesMerge() { let s = GroupingService(); let a = Detection(id: UUID(), classId: 0, className: "apple", confidence: 0.9, box: CGRect(x: 0.1, y: 0.1, width: 0.1, height: 0.1)); let b = Detection(id: UUID(), classId: 0, className: "apple", confidence: 0.8, box: CGRect(x: 0.19, y: 0.1, width: 0.1, height: 0.1)); XCTAssertEqual(s.group([a,b]).first?.count, 2) }
}
