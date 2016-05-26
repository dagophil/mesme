#include "mmMainWindow.h"

namespace mm
{

  MainWindow::MainWindow(QGuiApplication& app)
    : app_(app), view_(QUrl("qrc:/ui/mmMainWindow.qml"))
  {
    view_.show();
  }

} // namespace mm
