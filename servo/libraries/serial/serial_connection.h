#ifndef SERIAL_CONNECTION_H
#define SERIAL_CONNECTION_H

class SerialConnection {
public:
  SerialConnection();

  void setConnected();
  bool isConnected() const;

private:
  bool connected;
};

#endif
