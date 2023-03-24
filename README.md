# joystick_control_comovi

joystick control algorithm for comovi (indoor mobile robot)

![image](https://user-images.githubusercontent.com/63506664/227423358-ee1c8b00-3e1e-4b22-b1da-9c108bc90c1b.png)


## Functions

Index | Key map | Description | Range
---|---|---|---|
axes [0, 1] | Left Wheel Control | Left Wheel Speed (x, y direction) | -32767 ~ 32767
axes [3, 4] | Right Wheel Control | Right Wheel Speed (x, y direction) | -32767 ~ 32767
axes [6] | Simple Control | x direction: rotation (right, left) | -32767, 32767 (not gradual)
axes [7] | Simple Control | y direction: simple straight, back | -32767, 32767 (not gradual)
buttons [0] | Auto Drive Mode | Switch to Auto-drive mode (ignore joystick command) | 0, 1
buttons [1] | Emergency Stop | Emergency Stop (speed = 0) | 0, 1
buttons [2] | Manual Drive Mode | Switch to Manual-drive mode (follow joystick command) | 0, 1

## rqt_graph for Joystick control
![image](https://user-images.githubusercontent.com/63506664/227426678-8ccdbf2b-4922-43ac-b130-1a0739cc0bcd.png)
