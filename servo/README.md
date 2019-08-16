### Main commands

```sh
# Build
make 

# Upload sketch to board
make upload
```

Makefile full [documentation](https://github.com/sudar/Arduino-Makefile).


### Communication

The servo expects to receive commands via the Serial port, such as:

```sh
HELLO: 10
SET_SERVO_ANGLE: 31 + [16 bits integer]
```

It is typically controlled from the platform controller or its utilities.
