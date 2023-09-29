import os


class SetupFolder:
    def __init__(self, path, movmentName, noFile=30):
        for sequence in range(noFile):
            try:
                if not os.path.exists(os.path.join(path, movmentName, str(sequence))):
                    os.makedirs(os.path.join(path, movmentName, str(sequence)))
                else:
                    pass
            except FileExistsError:
                pass


if __name__ == '__main__':
    SetupFolder('../../data/train_data', ['goodbye', 'hello'], noFile=30)
