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

### 3. 一鍵編譯與除錯
- 您可以按下 `F5`，VS Code 將會自動觸發 CMake build 並以 Debug 模式啟動 `main.cpp` 產生出來的執行檔 (`MyPackageApp`)。
- 或是在 VS Code 下方的狀態列點擊 `Build` 來編譯，點擊 `Run` 來執行，點擊 `Debug` 圖示旁的蟲子按鈕來除錯。

## 自訂 Debug 優化層級
預設情況下，CMake 的 `Debug` 模式編譯為 `-O0`。如果你想要切換成 `-O1` 或 `-O2`：
1. 打開 `.vscode/settings.json`。
2. 找到 `cmake.configureArgs` 陣列。
3. 將 `-DDEBUG_OPT_LEVEL=O0` 修改為 `O1` 或 `O2`。
4. 儲存後，CMake Tools 會自動重新 Configure，並且在 Debug 模式套用你的設定檔。

## 打包成單一檔案 (Amalgamation)
如果你希望將分散在 `include/` 和 `src/` 中的源碼變成只要把一個 `.h` 和 `.cpp` 丟進別人專案就能用的格式（例如 SQLite 那樣）：

- **VS Code 任務方式**：按下 `Ctrl+Shift+B`（macOS: `Cmd+Shift+B`），選擇 `package single file`，這會呼叫 CMake 幫你執行 python 打包。
- **純 CMake 方式**：
  ```bash
  mkdir build && cd build
  cmake ..
  cmake --build . --target amalgamate
  ```

成功後，請查看專案根目錄下的 `dist/` 資料夾，裡面會產生：
- `mypackage_single.h`
- `mypackage_single.cpp`

你現在可以把這兩個檔案當成一個 Package 發布出去。這兩個檔案可以直接放入其他的專案並以 C++11 標準編譯：
```bash
g++ -std=c++11 test_main.cpp mypackage_single.cpp -o app
```
