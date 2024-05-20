class Golay:
    def __init__(self):
        self.k = 12
        self.n = 24
        self.s = [0] * 12
        self.r = [0] * 24
        self.P = [
            [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
            [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],
            [0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
            [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
        self.G = []
        self.HT = []
        self.get_matrices()

    @staticmethod
    def bin_add(a: int, b: int) -> int:
        return (a + b) % 2

    @staticmethod
    def bin_mul(a: int, b: int) -> int:
        return (a * b) % 2

    @staticmethod
    def weight(v: []) -> int:
        w = 0
        for i in range(12):
            w += v[i]
        return w

    def get_matrices(self):
        for i in range(12):
            self.G.append([0] * 24)
        for i in range(24):
            self.HT.append([0] * 12)
        I = []

        for i in range(12):
            I.append([])
            for j in range(12):
                I[i].append(1 if (i == j) else 0)

        for i in range(12):
            for j in range(24):
                if j < 12:
                    self.HT[j][i] = self.P[i][j]
                    self.G[i][j] = I[i][j]
                else:
                    self.G[i][j] = self.P[i][j - 12]
                    self.HT[j][i] = I[i][j - 12]
        print()

    def encode(self, message: []):
        print("Encoded codeword: ", end='')
        for i in range(24):
            for j in range(12):
                self.r[i] = self.bin_add(self.r[i], self.bin_mul(message[j], self.G[j][i]))
            print(self.r[i], end='')
        print()

    def add_errors(self):
        print("\nSending through a noisy channel...")
        positions = []
        print("How many errors? (in case of odd number >= 5, decoding error will occur):")
        num = int(input())
        for i in range(num):
            print(f"Position {i + 1}: ", end='')
            positions.append(int(input()))

        print("Adding errors in positions: ", end='')
        for i in range(num):
            self.r[positions[i]] = self.bin_add(self.r[positions[i]], 1)
            print(f"{positions[i]} ", end='')
        print("\nReceived message: ", end='')
        for i in range(24):
            print(self.r[i], end='')
        print()

    def get_syndrome(self):
        for i in range(24):
            for j in range(12):
                self.s[j] = self.bin_add(self.s[j], self.bin_mul(self.r[i], self.HT[(i + 12) % 24][j]))
        print("Syndrome: ", end='')
        for i in range(12):
            print(self.s[i], end='')
        print()

    def print_result(self, e: []):
        print("Error pattern: ", end='')
        for i in range(24):
            print(e[i], end='')
        print("\nDecoded codeword: ", end='')
        for i in range(24):
            print(self.bin_add(self.r[i], e[i]), end='')
        print()

    def decode(self):
        self.get_syndrome()
        e = [0] * 24
        print("Trying to decode...")
        if self.weight(self.s) <= 3:
            for i in range(24):
                if i < 12:
                    e[i] = self.s[i]
                else:
                    e[i] = 0
            print(f"w(s) = {self.weight(self.s)} <= 3")
            self.print_result(e)
            return

        for i in range(12):
            spi = [0] * 12
            for j in range(12):
                spi[j] = self.bin_add(self.s[j], self.P[i][j])
            if self.weight(spi) <= 2:
                for j in range(24):
                    if self.k < 12:
                        e[self.k] = spi[self.k]
                    else:
                        e[self.k] = (int(i == self.k) - 12)
                print(f"w(s + p{i}) = {self.weight(spi)} <= 2")
                self.print_result(e)
                return

        sp = [0] * 12
        for i in range(12):
            for j in range(12):
                sp[j] = self.bin_add(sp[j], self.bin_mul(self.s[i], self.P[i][j]))

        if self.weight(sp) == 2 or self.weight(sp) == 3:
            for i in range(24):
                if i < 12:
                    e[i] = 0
                else:
                    e[i] = sp[i - 12]
            print(f"w(s*P) = {self.weight(sp)}")
            self.print_result(e)
            return

        for i in range(12):
            sppi = [0] * 12
            for j in range(12):
                sppi[j] = self.bin_add(sp[j], self.P[i][j])
            if self.weight(sppi) == 2:
                for j in range(24):
                    if self.k < 12:
                        e[self.k] = int(i == self.k)
                    else:
                        e[self.k] = sppi[self.k - 12]
                print(f"w(s*P + p{i}) = {self.weight(sppi)}")
                self.print_result(e)
                return

        print("ERROR: Message Undecodable. Requesting retransmission...")
