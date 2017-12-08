import numpy as np
from pandas import * #NOT import, just used to visualize table easier
class Viterbi:
    def __init__(self, initial, states, obs, possible_obs, trans, emiss):
        self.initial = initial
        self.states = states
        self.obs = obs
        self.possible_obs = possible_obs
        self.trans = trans
        self.emiss = emiss
        self.num_states = len(self.states)
        self.num_obs = len(self.obs)
        self.table = np.zeros((self.num_states, self.num_obs + 1))
        self.backtrack_table = np.empty((self.num_states, self.num_obs), dtype="U16")
        self.backtrack = [self.num_states]
        self.backtrack_probabilites = []

    def run(self):
        #START VITERBI
        path = []
        #set the initial values to the start of the table
        for st in range(self.num_states):
            self.table[st][0] = self.initial[st]
        #find the value for each state at each time
        for ob in range(self.num_obs):
            observed = self.possible_obs.index(self.obs[ob])
            for i in range(self.num_states):
                prob = []
                save_state = 0
                save_max = 0
                for j in range(self.num_states):
                    prob.append(self.table[j][ob] * self.trans[i][j] * self.emiss[i][observed])
                    #there is probably a better way to do this...
                    if j == 0:
                        save_max = prob[0]
                    elif prob[j] > save_max:
                        save_max = prob[j]
                        save_state = j
                self.backtrack_table[i][ob] = self.states[save_state]
                self.table[i][ob + 1] = max(prob)
        #END VITERBI
        #START BACKTRACK
        #get most probable state in the last observation
        backtrack = []
        for i in range(self.num_obs, -1, -1):
            prob = []
            save_max = 0
            tmp = 0
            for j in range(self.num_states):
                prob.append(self.table[j][i])
                if(self.table[j][i] > prob[save_max]):
                    save_max = j
                tmp += self.table[j][i]
            backtrack.append(self.states[save_max])
            self.backtrack_probabilites.append(self.table[save_max][i]/tmp)

        #make more readable by reversing
        self.backtrack = backtrack[::-1]
        self.backtrack_probabilites = self.backtrack_probabilites[::-1]
        #END BACKTRACK

    def print_table(self):
        df = DataFrame(self.table)
        df.columns = ['Time 0'] + self.obs
        print("Probability Table")
        print(df)

    def print_backtrack_table(self):
        df = DataFrame(self.backtrack_table)
        df.columns = self.obs
        print("Backtrack Table")
        print(df)

    def print_backtrack(self):
        print("The most probable sequence of states is: ", end='')
        for bt in self.backtrack:
            print(bt + " ", end='')
        print("")

    def get_backtrack(self):
        return self.backtrack

    def get_backtrack_probabilites(self):
        return self.backtrack_probabilites

# if __name__ == "__main__":
#     states = ["Balanced", "Loaded_Heads", "Loaded_Tails"]
#     obs = ["Tails", "Tails", "Heads", "Heads", "Tails"]
#     possible_obs = ["Heads", "Tails"]
#     initial = [0.333, 0.333, 0.333]
#     #   trans matrix follows the following pattern:
#     #       [[balanced->balanced, loaded_heads->balanced, loaded_tails->balanced],
#     #       [balanced->loaded_heads, loaded_heads->loaded_heads, loaded_tails->loaded_heads],
#     #       [balanced->loaded_tails, loaded_heads->loaded_tails, loaded_tails->loaded_tails]]
#     trans = [[0.45, 0.52, 0.25], [0.35, 0.3, 0.13], [0.2, 0.18, 0.62]]
#     #   emiss matrix follows the following pattern:
#     #   [[balanced->heads, balanced->tails], [loaded_heads->heads, loaded_heads->tails] ...]
#     emiss = [[0.5, 0.5], [0.85, 0.15], [0.1, 0.9]]
#     v = Viterbi(initial, states, obs, possible_obs, trans, emiss)
#     v.run()
#     v.print_table()
#     v.print_backtrack_table()
#     v.print_backtrack()
# if __name__ == "__main__":
#     initial = [0.5, 0.5]
#     states = ["Buy", "Sell"]
#     obs = ["Up", "Up", "Down"]
#     possible_obs = ["Up", "Down"]
#     trans = [[0.5, 0.5], [0.5, 0.5]]
#     emiss = [[0.5, 0.5], [0.5, 0.5]]
#     v = Viterbi(initial, states, obs, possible_obs, trans, emiss)
#     v.run()
#     v.print_table()
#     v.print_backtrack_table()
#     v.print_backtrack()
