#include "serial_connection.h"
#include "serial_io.h"

SerialConnection::SerialConnection() : connected(false) {
}

void SerialConnection::setConnected() {
  this->connected = true;
}

bool SerialConnection::isConnected() const {
  return this->connected;
}
