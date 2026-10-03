import pytest

from ai_master.logistic import LogisticRegression
from ai_master.metrics import accuracy, macro_f1, rmse
from ai_master.retrieval import TfidfRetriever, tokenize


def test_logistic_regression_learns_and_loss_decreases():
    model = LogisticRegression(learning_rate=0.8, epochs=300).fit([[0, 0], [0, 1], [1, 0], [1, 1]], [0, 0, 0, 1])
    assert model.history[-1] < model.history[0]
    assert accuracy([0, 0, 0, 1], model.predict([[0, 0], [0, 1], [1, 0], [1, 1]])) >= 0.75


def test_logistic_regression_rejects_invalid_training_parameters():
    for parameter in ({"epochs": 0}, {"epochs": -1}, {"learning_rate": 0}, {"l2": -0.1}):
        with pytest.raises(ValueError):
            LogisticRegression(**parameter).fit([[0.0], [1.0]], [0, 1])


def test_metrics_and_input_validation():
    assert macro_f1([0, 1, 1], [0, 1, 0]) == pytest.approx(0.666666, rel=1e-4)
    assert rmse([1.0, 3.0], [1.0, 1.0]) == pytest.approx(2**0.5)
    with pytest.raises(ValueError):
        accuracy([], [])


def test_retriever_returns_relevant_document_and_handles_unicode():
    assert "học" in tokenize("Học máy")
    retriever = TfidfRetriever(["gradient descent optimises a loss", "retrieval finds relevant documents"])
    assert retriever.search("relevant documents", k=1)[0][0] == 1
    with pytest.raises(ValueError):
        retriever.search("query", k=0)
