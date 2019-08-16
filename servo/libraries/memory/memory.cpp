#include <EEPROM.h>

#include "memory.h"
#include "memory_parameters.h"
#include "serial_io.h"

void Memory::setIdentifier(int8_t identifier) {
  EEPROM.get(DATA_ADDRESS, this->data);
  this->data.identifier = identifier;

  EEPROM.put(DATA_ADDRESS, this->data);
  println("Identifier set: " + String(identifier));
}

int8_t Memory::getIdentifier() const {
  EEPROM.get(DATA_ADDRESS, this->data);
  return this->data.identifier;
}

void Memory::setZeroRawPosition(uint8_t rawPosition) {
  EEPROM.get(DATA_ADDRESS, this->data);
  this->data.zeroRawPosition = rawPosition;

  EEPROM.put(DATA_ADDRESS, this->data);
  println("Zero raw position set: " + String(rawPosition));
}

uint8_t Memory::getZeroRawPosition() const {
  EEPROM.get(DATA_ADDRESS, this->data);
  return this->data.zeroRawPosition;
}
