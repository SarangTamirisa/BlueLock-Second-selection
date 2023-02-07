import numpy as np


# Write code for second selection

class SecondSelection:
    def __init__(self, n, p_per_t_initial, quali_n, disquali_n):
        self.playing_rows = None
        self.n_p = n  # total number of players
        self.p_per_t_initial = p_per_t_initial  # initial number of players per team

        self.start_n = self.p_per_t_initial
        self.quali_n = quali_n
        self.disquali_n = disquali_n
        self.num_stages = self.quali_n - self.disquali_n + 1
        table_zero = np.zeros(self.num_stages, int)
        self.start_n_ind = self.start_n - self.disquali_n
        table_zero[self.start_n_ind] = self.n_p
        self.table_init = table_zero
        self.finalized = False
        self.k = 0
        self.n = 0

    def selection(self):
        c_table = self.table_init

        self.playing_rows = self.quali_n - self.disquali_n

        while not self.finalized:
            print(c_table)
            j = 0
            for i in range(1, self.playing_rows):

                if c_table[i] == 0:
                    j += 1

            if j == self.playing_rows - 1:

                self.finalized = True

            else:
                u_table = self.execute_match(c_table)

                c_table = u_table
                self.finalized = False
                self.k += 1

    def execute_match(self, table):

        add_tab = np.zeros(self.num_stages, int)
        m = 0
        for i in range(1, self.playing_rows):
            if table[i] != 0:
                n = int(table[i])
                if n < 2 * (i + self.disquali_n):
                    m += 1
                if n >= 2 * (i + self.disquali_n):
                    num_top, num_bottom = self.matches(n, (i + self.disquali_n))
                else:
                    num_top = num_bottom = 0
            else:
                num_top = num_bottom = 0
                m += 1
            if m < self.playing_rows - 1:
                add_tab[i - 1] = add_tab[i - 1] + num_bottom
                add_tab[i] = add_tab[i] - num_top - num_bottom
                add_tab[i + 1] = add_tab[i + 1] + num_top
            else:
                print("Gather")
                add_tab = self.final_rounds(table)

        u_table = table + add_tab
        # print("executed", add_tab)
        return u_table


    def matches(self, n, s):
        # print("")

        team_size = s
        two_team_size = 2 * team_size
        n_back = n % two_team_size
        n_modified = n - n_back
        num_matches = n_modified / two_team_size
        self.n = self.n + num_matches
        num_top = num_matches * (team_size + 1)
        num_bottom = num_matches * (team_size - 1)

        return num_top, num_bottom

    def final_rounds(self, table):
        n = 0
        add_tab = np.zeros(self.num_stages, int)
        for i in range(1, self.playing_rows):
            n = n + table[i]

        if n < 2 * (self.quali_n - 1):
            for i in range(1, self.playing_rows):
                add_tab[i] = add_tab[i] - table[i]
            add_tab[0] = add_tab[0] + n
        else:

            for i in range(1, self.playing_rows):
                add_tab[i] = add_tab[i] - table[i]

            add_tab[self.num_stages - 2] = n - table[self.num_stages - 2]
        return add_tab


if __name__ == '__main__':
    # ( total number of players, starting size of the team, Qualifying team size, Disqualifying team size )
    Bluelock = SecondSelection(111, 3, 5, 1)
    Bluelock.selection()
    print(Bluelock.n)
