import os

import torch
import random
import numpy as np
from collections import deque
from game import BrickBreakerGameAI
from model import Linear_QNet, QTrainer
import matplotlib.pyplot as plt
from IPython import display

plt.ion()

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0  # control randomness
        self.gamma = 0.9  # discount rate, should be < 1
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft if reach max
        self.model = Linear_QNet(8, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        # self.load_training()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of BATCH_SIZE tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.number_of_games
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        return move

    def save_training(self, filename='training.pth'):
        training_folder_path = './training'
        if not os.path.exists(training_folder_path):
            os.makedirs(training_folder_path)
        filename = os.path.join(training_folder_path, filename)
        torch.save({
            'epoch': self.number_of_games,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.trainer.optimizer.state_dict()
        }, filename)

    def load_training(self, filename='training.pth'):
        training_folder_path = './training'
        filename = os.path.join(training_folder_path, filename)
        if os.path.exists(filename):
            checkpoint = torch.load(filename)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.trainer.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        else:
            print("No saved model found. Starting from scratch.")


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    best_score = 0
    agent = Agent()
    game = BrickBreakerGameAI()
    while True:
        # Get old state
        state_old = get_game_state(game)

        # Get move
        final_move = agent.get_action(state_old)

        # Perform move and get new state
        reward, game_over, score = game.step(final_move)
        state_new = get_game_state(game)

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # Remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        # Check game over
        if game_over:
            # Train Long Memory, plot result
            game.reset()
            agent.number_of_games += 1
            agent.train_long_memory()
            if score > best_score:
                best_score = score
                agent.save_training()

            print(f"Game: {agent.number_of_games} | Score: {score} | Best Score: {best_score}")

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


def get_game_state(game):
    ball_x = game.current_stage.ball.rect.x
    ball_y = game.current_stage.ball.rect.y
    ball_vx = game.current_stage.ball.direction.x
    ball_vy = game.current_stage.ball.direction.y
    paddle_x = game.current_stage.paddle.rect.x

    relative_x = ball_x - paddle_x
    relative_y = ball_y - game.current_stage.paddle.rect.y

    # Calculate the angle of the ball's trajectory relative to the paddle
    angle = np.arctan2(ball_vy, ball_vx)  # Angle in radians

    state = [
        ball_x,
        ball_y,
        ball_vx,
        ball_vy,
        paddle_x,
        relative_x,
        relative_y,
        angle
    ]
    return np.array(state, dtype=float)


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


if __name__ == '__main__':
    train()
