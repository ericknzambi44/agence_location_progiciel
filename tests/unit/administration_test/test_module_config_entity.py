import pytest
from administration.domain.entities.module_config import ModuleConfig
from administration.domain.value_objects.code_module import CodeModule

def test_creer_module():
    code = CodeModule("STOCK")
    module = ModuleConfig(code=code, nom="Gestion des stocks")
    # On convertit en majuscule pour la comparaison, au cas où CodeModule ne le ferait pas
    assert module.code.value.upper() == "STOCK"