# Hand Tracking Snake Game with AI-Powered Obstacle Detection

## Overview

This project is a computer vision game developed in Python that combines hand tracking technology using MediaPipe with a snake game logic. The snake's movement is controlled by the user's index finger, and the objective is to score points by touching the green bait. The game incorporates artificial intelligence to detect and introduce red obstacles that players must avoid.

## Features

- Hand tracking for controlling the snake's movement.
- Snake game logic with a scoring system.
- AI-powered obstacle detection for adding challenging elements.
- Green bait for scoring points and red obstacles to avoid.

## Files

This repository includes the following files:

- `hand_tracking_snake_game.py`: Python script for the hand tracking snake game.

## Usage

To run the game, follow these steps:

1. Install the required dependencies: `mediapipe`, `cv2`, `numpy`, `time`, and `random`.
2. Run the Python script: `python hand_tracking_snake_game.py`.
3. Use your index finger to control the snake and score points.

## How to Play

- Press 'Q' to quit the game.
- Score points by touching the green bait.
- Avoid red obstacles to prevent the game from ending.

## Rules

1. The game will end if the snake collides with a red obstacle.
2. The bait will reappear in a new location after being touched.
3. Each successful touch increases the snake's length and difficulty.
