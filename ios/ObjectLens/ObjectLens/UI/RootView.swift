import SwiftUI
struct RootView: View { var body: some View { TabView { CameraView().tabItem { Text("Камера") }; GalleryView().tabItem { Text("Изображение") }; HistoryView().tabItem { Text("История") }; SettingsView().tabItem { Text("Настройки") } } } }
struct CameraView: View { var body: some View { ZStack { Color.black.ignoresSafeArea(); Text("Object Lens").foregroundStyle(.white).font(.largeTitle.bold()) } } }
struct GalleryView: View { var body: some View { NavigationStack { ContentUnavailableView("Выбор изображения", systemImage: "photo", description: Text("Photo Picker использует ограниченный доступ без запроса всей медиатеки.")) } } }
struct HistoryView: View { var body: some View { NavigationStack { ContentUnavailableView("История пуста", systemImage: "clock", description: Text("Сохранённые распознавания появятся здесь.")) } } }
struct SettingsView: View { @AppStorage("haptics") var haptics = true; var body: some View { NavigationStack { Form { Toggle("Вибрация", isOn: $haptics); Text("Акцентный цвет: нейтральный зелёный") } .navigationTitle("Настройки") } } }
