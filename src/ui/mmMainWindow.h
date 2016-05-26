#ifndef MM_MAIN_WINDOW_H
#define MM_MAIN_WINDOW_H

#include <memory>

#include <QObject>
#include <QGuiApplication>
#include <QQuickView>

namespace mm
{
  class MainWindow : QObject
  {
    Q_OBJECT

  public:

    MainWindow(QGuiApplication& app);

  private:

    QGuiApplication& app_;
    QQuickView view_;


  }; // class MainWindow
} // namespace mm

#endif
