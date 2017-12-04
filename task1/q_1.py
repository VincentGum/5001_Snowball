# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:26:34 2017

compute the rsi of every industry and save as a csv

@author: VincentGum
"""

import numpy as np
import pandas as pd


class q_unit():
    """
    STATES is a pandas.DataFrams, with each row for each day, each column for features
    ACTIONS is a list
    """
    STATES = pd.DataFrame
    ACTIONS = []  # 探索者的可用动作
    REWARD_RULE = pd.DataFrame
    EPSILON = 0.6  # 贪婪度 greedy
    ALPHA = 0.1  # 学习率
    GAMMA = 0.9  # 奖励递减值
    MAX_EPISODES = 0  # 最大回合数
    FRESH_TIME = 0.3  # 移动间隔时间

    STRATEGY = []

    def __init__(self, STATES, ACTIONS, REWARD_RULE, EPSILON=0.9, ALPHA=0.1, GAMMA=0.9, MAX_EPISODES=500, FRESH_TIME=0.3):
        self.STATES = STATES
        self.ACTIONS = ACTIONS
        self.REWARD_RULE = REWARD_RULE
        self.EPSILON = EPSILON
        self.ALPHA = ALPHA
        self.GAMMA = GAMMA
        self.MAX_EPISODES = MAX_EPISODES
        self.FRESH_TIME = FRESH_TIME

    def build_q_table(self, n_states, actions):
        table = pd.DataFrame(
            np.zeros((n_states, len(actions))),  # q_table 全 0 初始
            columns=actions,  # columns 对应的是行为名称
        )
        return table

    def choose_action(self, state, q_table):
        state_actions = q_table.iloc[state, :]  # 选出这个 state 的所有 action 值
        if (np.random.uniform() > self.EPSILON) or (state_actions.all() == 0):  # 非贪婪 or 或者这个 state 还没有探索过
            action_name = np.random.choice(self.ACTIONS)
        else:
            action_name = state_actions.argmax()  # 贪婪模式
        self.STRATEGY.append(action_name)
        return action_name

    def get_env_feedback(self, stepcounter, A):
        # This is how agent will interact with the environment
        R = 0
        ins = A

        if stepcounter == len(self.STATES) - 2:  # terminate
            S_ = 'terminal'

            if (0 <= self.REWARD_RULE[stepcounter][ins]) & (self.REWARD_RULE[stepcounter][ins] < 30):
                R += 10
            elif (30 <= self.REWARD_RULE[stepcounter][ins]) & (self.REWARD_RULE[stepcounter][ins] < 70):
                R += 2

        else:
            S_ = self.STATES.loc[stepcounter + 1]

            if (0 <= self.REWARD_RULE[stepcounter][ins]) & (self.REWARD_RULE[stepcounter][ins] < 30):
                R += 10
            elif (30 <= self.REWARD_RULE[stepcounter][ins]) & (self.REWARD_RULE[stepcounter][ins] < 70):
                R += 2

        return S_, R

    def rl(self):
        q_table = self.build_q_table(len(self.STATES) - 10, self.ACTIONS)  # 初始 q table


        for episode in range(self.MAX_EPISODES):  # 回合
            print(episode)
            step_counter = 10
            S = self.STATES.loc[10]  # 回合初始位置
            is_terminated = False
            self.STRATEGY = []

            while not is_terminated:

                A = self.choose_action(step_counter, q_table)  # 选行为
                S_, R = self.get_env_feedback(step_counter, A)  # 实施行为并得到环境的反馈
                q_predict = q_table.ix[step_counter, A]  # 估算的(状态-行为)值

                if step_counter != 657:
                    q_target = R + self.GAMMA * q_table.iloc[step_counter + 1, :].max()  # 实际的(状态-行为)值 (回合没结束)

                else:
                    q_target = R  # 实际的(状态-行为)值 (回合结束)
                    is_terminated = True  # terminate this episode

                q_table[A][step_counter] += self.ALPHA * (q_target - q_predict)  # q_table 更新
                S = S_  # 探索者移动到下一个 state
                step_counter += 1

        return q_table

    def learn(self):
        q_table = self.rl()
        return q_table, self.STRATEGY