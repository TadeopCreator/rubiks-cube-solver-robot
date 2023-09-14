# Rubik's Cube Solver Robot

This repository contains the code for a Rubik's Cube solver robot project. The project involves developing both the user interface (implemented in Python using Tkinter) and the embedded system control code (written in C) to control the stepper motors and other hardware components.

## Overview

The Rubik's Cube Solver Robot is designed to solve a 3x3 Rubik's Cube autonomously. It uses a combination of hardware components, including stepper motors, a microcontroller, and Bluetooth communication, along with software components for interface and control.

## Components

The project consists of the following major components:

- **User Interface (Python):** The user interface allows users to interact with the robot. It provides options for manual cube state input, automatic color detection using computer vision, and initiating the cube-solving process.

- **Embedded System Control (C):** The embedded system control code runs on the microcontroller (EDU CIAA NXP). It interprets the solution sequence and controls the stepper motors to solve the Rubik's Cube.

- **Bluetooth Communication:** The robot communicates with the user interface via Bluetooth (HC-05 module) to receive cube state data and transmit the solution sequence.

- **Hardware (PCB, Motors, Drivers):** The hardware includes a custom PCB, NEMA17 stepper motors, A4988 motor drivers, a 12V external power supply, and additional components for structural support.

## Getting Started

To get started with the project, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the respective directories (`interface` for the Python code and `embedded_system` for the C code) and follow the setup instructions provided in those directories.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

We would like to acknowledge the support of our team members and the guidance of our instructors in completing this project.
