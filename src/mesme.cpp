#include "ui/mmMainWindow.h"

#include <QGuiApplication>

int main(int argc, char** argv)
{
  QGuiApplication app(argc, argv);
  mm::MainWindow main_window(app);
  return app.exec();
}
