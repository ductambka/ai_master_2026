from __future__ import annotations

import argparse

from .logistic import LogisticRegression
from .metrics import accuracy
from .retrieval import TfidfRetriever


def demo() -> None:
    x = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    y = [0, 0, 0, 1]
    model = LogisticRegression(learning_rate=0.8, epochs=300).fit(x, y)
    predictions = model.predict(x)
    print(f"logistic_accuracy={accuracy(y, predictions):.3f}; final_loss={model.history[-1]:.4f}")
    retriever = TfidfRetriever(["gradient descent optimises a loss", "retrieval finds relevant documents", "evaluation needs a held out test set"])
    print(f"retrieval={retriever.search('relevant documents', k=2)}")


def train(epochs: int) -> None:
    model = LogisticRegression(learning_rate=0.8, epochs=epochs).fit([[0, 0], [0, 1], [1, 0], [1, 1]], [0, 0, 0, 1])
    print(f"epochs={epochs}; final_loss={model.history[-1]:.6f}; weights={model.weights}; bias={model.bias:.6f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Master practical reference CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("demo")
    train_parser = subparsers.add_parser("train")
    train_parser.add_argument("--epochs", type=int, default=100)
    args = parser.parse_args()
    if args.command == "demo":
        demo()
    else:
        train(args.epochs)


if __name__ == "__main__":
    main()

