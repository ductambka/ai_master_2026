import pytest

from ai_master.logistic import LogisticRegression
from ai_master.metrics import accuracy, confusion_matrix, macro_f1, rmse
from ai_master.retrieval import TfidfRetriever, tokenize


def test_logistic_regression_learns_and_loss_decreases():
    model = LogisticRegression(learning_rate=0.8, epochs=300).fit([[0, 0], [0, 1], [1, 0], [1, 1]], [0, 0, 0, 1])
    assert model.history[-1] < model.history[0]
    assert accuracy([0, 0, 0, 1], model.predict([[0, 0], [0, 1], [1, 0], [1, 1]])) >= 0.75


def test_logistic_regression_rejects_invalid_training_parameters():
    for parameter in (
        {"epochs": 0},
        {"epochs": -1},
        {"learning_rate": 0},
        {"learning_rate": True},
        {"learning_rate": "fast"},
        {"l2": -0.1},
        {"l2": False},
        {"l2": "none"},
    ):
        with pytest.raises(ValueError):
            LogisticRegression(**parameter).fit([[0.0], [1.0]], [0, 1])

    with pytest.raises(ValueError, match="rectangular"):
        LogisticRegression().fit([[], []], [0, 1])

    with pytest.raises(ValueError, match="finite numeric"):
        LogisticRegression().fit([[0.0], [float("nan")]], [0, 1])
    with pytest.raises(ValueError, match="binary labels"):
        LogisticRegression().fit([[0.0], [1.0]], [False, True])

    with pytest.raises(ValueError, match="rectangular matrix"):
        LogisticRegression().fit([None], [0])  # type: ignore[list-item]
    with pytest.raises(ValueError, match="lists"):
        LogisticRegression().fit(((0.0,), (1.0,)), [0, 1])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="lists"):
        LogisticRegression().fit([[0.0], [1.0]], (0, 1))  # type: ignore[arg-type]


def test_logistic_regression_rejects_non_finite_prediction_features():
    model = LogisticRegression().fit([[0.0], [1.0]], [0, 1])
    with pytest.raises(ValueError, match="row must be a list"):
        model.predict_proba_one(None)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="row must be a list"):
        model.predict_proba_one((0.0,))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="finite numeric"):
        model.predict_proba_one([float("inf")])
    with pytest.raises(ValueError, match="only rows"):
        model.predict([None])  # type: ignore[list-item]
    with pytest.raises(ValueError, match="between 0 and 1"):
        model.predict([[0.0]], threshold=float("nan"))

    with pytest.raises(ValueError, match="not fitted"):
        LogisticRegression().predict([])


def test_metrics_and_input_validation():
    assert macro_f1([0, 1, 1], [0, 1, 0]) == pytest.approx(0.666666, rel=1e-4)
    assert rmse([1.0, 3.0], [1.0, 1.0]) == pytest.approx(2**0.5)
    with pytest.raises(ValueError):
        accuracy([], [])
    with pytest.raises(ValueError, match="integers"):
        accuracy([1], [True])
    with pytest.raises(ValueError, match="finite numbers"):
        rmse([1.0], [float("inf")])
    assert confusion_matrix((0, 1, 1), iter((0, 0, 1))) == {(0, 0): 1, (1, 0): 1, (1, 1): 1}
    with pytest.raises(ValueError, match="same non-zero length"):
        confusion_matrix([0, 1], [0])
    with pytest.raises(ValueError, match="integers"):
        confusion_matrix([0], [False])


def test_retriever_returns_relevant_document_and_handles_unicode():
    assert "học" in tokenize("Học máy")
    retriever = TfidfRetriever(["gradient descent optimises a loss", "retrieval finds relevant documents"])
    assert retriever.search("relevant documents", k=1)[0][0] == 1
    with pytest.raises(ValueError):
        retriever.search("query", k=0)
    with pytest.raises(ValueError, match="non-empty"):
        TfidfRetriever([])
    with pytest.raises(ValueError, match="non-empty strings"):
        TfidfRetriever(["valid document", "  "])
    with pytest.raises(ValueError, match="searchable token"):
        TfidfRetriever(["!!!"])
    with pytest.raises(ValueError, match="string"):
        retriever.search(3)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="non-empty string"):
        retriever.search("   ")
    with pytest.raises(ValueError, match="searchable token"):
        retriever.search("!!!")
    with pytest.raises(ValueError, match="string"):
        tokenize(None)  # type: ignore[arg-type]
