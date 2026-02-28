# VS Code CMake Project Template (C++11)

這是一個全功能且跨平台的 CMake C++11 專案模板，專為 VS Code 所設計，保持乾淨純粹的環境。支援：

- **一鍵編譯與除錯 (One-click build and run)**
- **自訂 Debug 模式優化層級** (例如 `-O0`, `-O1`, `-O2`)
- **打包輸出成單一 `.h` 與 `.cpp` 檔案**

## 目錄結構
- `include/mypackage/`：對外公開的 C++ 標頭檔。
- `src/`：實作的原始碼以及主程式 `main.cpp`。
- `scripts/`：Python 輔助腳本 (用於打包單一檔案)。
- `dist/`：執行 `amalgamate` 目標後，輸出的單一檔案位置。
- `.vscode/`：VS Code 一鍵安裝與執行所需的設定。

## 環境需求
1. CMake (>= 3.12)
2. 編譯器支援 C++11 (GCC, Clang, 或 MSVC)
3. Python 3 (僅用於單一檔案打包腳本)

## 如何在 VS Code 中使用

### 1. 安裝推薦套件
當您用 VS Code 開啟此專案目錄時，右下角會提示安裝推薦的擴充套件（主要為 `C/C++` 以及 `CMake Tools`）。請點擊 **Install** 進行安裝。

### 2. 設定與選擇編譯器
按下 `Ctrl+Shift+P`（macOS: `Cmd+Shift+P`）輸入 `CMake: Select a Kit`，選擇您電腦上的 GCC/Clang 或 MSVC 編譯器。

### 3. 使用 CMake Presets 設定優化層級 (O0, O1, O2, O3)
本專案已經內建了 `CMakePresets.json`。在 VS Code 裡面修改優化層級最快的方式是：

1. 按下 `Ctrl + Shift + P` (macOS: `Cmd + Shift + P`) 開啟命令列。
2. 輸入並選擇 **`CMake: Select Configure Preset`**。
3. 您將會看到選單中列出了：`Debug-O0`, `Debug-O1`, `Debug-O2`, `Debug-O3` 以及 `Release`。
4. 選擇您想要的優化層級，CMake 會自動為您生成對應的設定。

> 您也可以在 VS Code 下方狀態列點選左方的 Configure 按鈕 (可能顯示為 `CMake: [Debug-O0]`) 進行切換。

### 4. 一鍵編譯與除錯
**⚠️ 重要：請不要直接按 F5 啟動除錯。** 這可能會觸發 VS Code 預設對單一檔案進行 GCC 編譯的錯誤行為。
請完全依靠 CMake Tools 擴充套件：
- 點擊 VS Code **下方狀態列**的 `Build` 來編譯所選目標 (Targets)。
- 點擊狀態列的 `Debug`（蟲子圖示）或是 `Run`（播放圖示）來執行主程式。
- （建議）您也可以開啟 VS Code **左側的 CMake 側邊欄**，找到 `MyPackageApp` 後點擊啟動或除錯圖示。

## 打包成單一檔案 (Amalgamation)
如果你希望將分散在 `include/` 和 `src/` 中的源碼打包成只要一個 `.h` 和 `.cpp` 就能放入別人專案的格式，我們提供了專屬的 CMake Preset 讓您一鍵打包：

1. 點擊 VS Code **下方狀態列的 Configure 預設檔名稱** (例如 `CMake: [Debug-O0]`)，或按下 `Ctrl+Shift+P` 選擇 `CMake: Select Configure Preset`。
2. 在選單中選擇 **`Amalgamate`** (Build Single File Package)。
3. CMake 會自動切換設定。接著點擊狀態列底下的 **`Build`** 按鈕，或是按下 `F7` 即可！

- **純 CMake 方式 (Command Line)**：
  ```bash
  cmake --preset Amalgamate
  cmake --build --preset Amalgamate
  ```

成功後，請查看專案根目錄下的 `dist/` 資料夾，裡面會產生：
- `mypackage_single.h`
- `mypackage_single.cpp`

你現在可以把這兩個檔案當成一個 Package 發布出去。這兩個檔案可以直接放入其他的專案並以 C++11 標準編譯：
```bash
g++ -std=c++11 test_main.cpp mypackage_single.cpp -o app
```
