# Rubik's Cube Solver Robot

This repository comprises the code for a Rubik's Cube solver robot project. The project involves developing both the user interface (implemented in Python using Tkinter) and the embedded system control code (written in C) to control the stepper motors and other hardware components.

## Media

<div align="center">
  <img src="https://github.com/TadeopCreator/rubiks-cube-solver-robot/blob/master/images/structure/structure.jpeg" alt="Structure Images" width="500"/>
  <img src="https://github.com/TadeopCreator/rubiks-cube-solver-robot/blob/master/images/edu_ciaa/edu_ciaa.jpeg" alt="Structure Images" width="500" style="margin-top: -200px;"/>
</div>

<div align="center">
  <img src="https://github.com/TadeopCreator/rubiks-cube-solver-robot/blob/master/images/cube_scanning/automatic_scan.png" alt="Cube Scanning Images" width="400"/>
  <img src="https://github.com/TadeopCreator/rubiks-cube-solver-robot/blob/master/images/cube_scanning/manual_setup.png" alt="Manual Setup" width="400"/>
</div>

<br>

[Project demo](https://github.com/TadeopCreator/rubiks-cube-solver-robot/tree/master/demo)

## Overview

The Rubik's Cube Solver Robot is designed to autonomously solve a 3x3 Rubik's Cube. It integrates hardware components like stepper motors, a microcontroller (EDU CIAA NXP), Bluetooth communication, and software components for interface and control.

## Components

The project consists of the following major components:

- **User Interface (Python):** Allows user interaction, manual cube state input, automatic color detection using computer vision, and initiating the cube-solving process.
  
- **Embedded System Control (C):** Runs on the EDU CIAA NXP microcontroller. It interprets the solution sequence and controls the stepper motors for solving the Rubik's Cube.

- **Bluetooth Communication:** Facilitates communication between the robot and the user interface via Bluetooth (HC-05 module) for receiving cube state data and transmitting the solution sequence.

- **Hardware (PCB, Motors, Drivers):** Includes a custom PCB, NEMA17 stepper motors, A4988 motor drivers, a 12V external power supply, and additional structural support components.

## Getting Started

To begin with the project:

1. Clone this repository to your local machine.
2. Navigate to the respective directories (interface for Python code and embedded_system for C code) and follow the setup instructions provided in those directories.

## Built With

This project was developed using the [EDU CIAA NXP microcontroller](https://github.com/ciaa) and was part of the "Taller de Proyecto 1" course at the Faculty of Engineering of UNLP.

## License

This project is licensed under the MIT License.

## Acknowledgments

We extend our gratitude to our team members and the guidance of our instructors in completing this project. Additionally, we drew inspiration and utilized information from the following repositories:

- [RubiksCube-TwophaseSolver](https://github.com/hkociemba/RubiksCube-TwophaseSolver)
- [qbr](https://github.com/kkoomen/qbr#example-runs)

