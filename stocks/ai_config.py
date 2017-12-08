states = ["Buy", "Sell"]
possible_obs = ["Up", "Down"]
#initial probabilty
#[buy, sell]
initial = [0.5, 0.5]

#transitive matrix
#[[buy->buy, buy->sell], [sell->buy, sell->sell]]
trans = [[0.5, 0.5], [0.5, 0.5]]

#emission matrix
#[[buy->up, buy->down], [sell->up, sell->down]]
emiss = [[0.8, 0.2], [0.2, 0.8]]
