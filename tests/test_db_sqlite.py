import os
import tempfile
from db import init_sqlite_db, seed_quizzes_from_config, save_quiz_result, get_aggregated_results, export_results_to_csv
import pandas as pd


def test_sqlite_seed_and_save(tmp_path):
    db_file = tmp_path / "test_cybercoach.db"
    db_path = str(db_file)

    # Init DB and seed quizzes
    assert init_sqlite_db(db_path)
    assert seed_quizzes_from_config(db_path=db_path)

    # Save a quiz result
    ok = save_quiz_result("user1", "IT", "phishing", 2, 2, {"1": 1, "2": 1}, db_path=db_path)
    assert ok is True

    # Get aggregated results
    df = get_aggregated_results(db_path=db_path)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # Export CSV
    out = tmp_path / "out.csv"
    ok = export_results_to_csv(str(out), db_path=db_path)
    assert ok is True
    assert out.exists()
