def test_process_reference_from_bibtex(decorated_with_bibtex):
    from r2t2 import BIBLIOGRAPHY
    from r2t2.reference_processors import BibtexProcessor

    BIBLIOGRAPHY.tracking()

    decorated_with_bibtex()
    BibtexProcessor(source="references.bib")
    assert "An amazing title by Jean César (2013)" in BIBLIOGRAPHY.references[-1]

    BIBLIOGRAPHY.clear()
    BIBLIOGRAPHY.tracking(False)
