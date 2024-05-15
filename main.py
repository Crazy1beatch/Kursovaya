import Golay


def run_program():
    g = Golay.Golay()
    message = []
    print("Message (separate digits new lines): ")
    for i in range(12):
        message.append(int(input()))
    g.encode(message)
    g.add_errors()
    g.decode()



if __name__ == '__main__':
    run_program()
