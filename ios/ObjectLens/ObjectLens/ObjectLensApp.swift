import SwiftUI
import SwiftData

@main
struct ObjectLensApp: App {
    var body: some Scene {
        WindowGroup { RootView().modelContainer(for: RecognitionRecord.self) }
    }
}
