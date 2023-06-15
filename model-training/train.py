from detecto.core import Model, Dataset

def main():
    dataset = Dataset("images/")

    model = Model(["toppables"])
    model.fit(dataset)
    model.save("toppables.pth")

if __name__ == "__main__":
    main()
