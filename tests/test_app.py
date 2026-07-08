from fastapi import FastAPI
import importlib


def test_app_imports():
    mod = importlib.import_module('app.main')
    assert hasattr(mod, 'app')
    assert isinstance(mod.app, FastAPI)
