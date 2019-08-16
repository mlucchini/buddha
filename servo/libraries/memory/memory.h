#ifndef MEMORY_H
#define MEMORY_H

struct Data {
  int8_t identifier;
  uint8_t zeroRawPosition;
};

class Memory {
public:
  void setIdentifier(int8_t identifier);
  int8_t getIdentifier() const;

  void setZeroRawPosition(uint8_t rawPosition);
  uint8_t getZeroRawPosition() const;

private:
  Data data;
};

#endif
