# Buddha

<p align="center">
  <img src="doc/demo.gif" alt="Buddha at work" style="border: 1px solid black">
  </br>
  Loop animation mode
</p>

### Servos

Upload the servo sketch to an Arduino board connected to a NVH2SP30 driver, an
ACE128 absolute position encoder and a DC motor (Opel Astra windshield wipers in my case).
Follow the controller's README to configure the servos appropriately.

```sh
cd servo
make upload
 
cd ../controller
cat README.md
```


### Controller

Copy the platform driver to a machine connected to the 6 servos:

```sh
cd controller
make copy
 
ssh pi@local
cd buddha
pip3 install -r requirements.txt
python3 cli-platform.py
 
# Example: simple roll movement performed in loop
animation 0 0 0 0.2 0 0 0.5 0 0 0 -0.2 0 0 0.5
```
