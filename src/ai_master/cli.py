from __future__ import annotations

import argparse
import json

from .evaluation import EvaluationError, evaluate_files
from .logistic import LogisticRegression
from .metrics import accuracy
from .retrieval import TfidfRetriever


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _unit_interval(value: str) -> float:
    parsed = float(value)
    if not 0 <= parsed <= 1:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return parsed


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
    train_parser.add_argument("--epochs", type=int, default=100, metavar="N", help="positive number of training epochs")
    evaluate_parser = subparsers.add_parser("evaluate", help="evaluate provider output against a JSONL gold set")
    evaluate_parser.add_argument("--gold", required=True, type=str)
    evaluate_parser.add_argument("--predictions", required=True, type=str)
    evaluate_parser.add_argument("--output", required=True, type=str)
    evaluate_parser.add_argument("--k", type=_positive_int, default=3)
    evaluate_parser.add_argument("--seed", type=int, default=0)
    evaluate_parser.add_argument("--semantic-threshold", type=_unit_interval, default=0.5)
    args = parser.parse_args()
    if args.command == "demo":
        demo()
    elif args.command == "train":
        if args.epochs < 1:
            parser.error("--epochs must be a positive integer")
        train(args.epochs)
    else:
        try:
            result = evaluate_files(args.gold, args.predictions, k=args.k, seed=args.seed, semantic_threshold=args.semantic_threshold)
        except (EvaluationError, OSError) as exc:
            parser.error(str(exc))
        try:
            with open(args.output, "w", encoding="utf-8") as output:
                json.dump(result, output, indent=2, sort_keys=True)
                output.write("\n")
        except OSError as exc:
            parser.error(f"cannot write evaluation output: {exc}")
        print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
