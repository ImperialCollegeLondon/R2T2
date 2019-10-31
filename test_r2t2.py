def fun_with_reference() -> None:
    from r2t2 import science_reference

    science_reference("doing something smart", "My Awesome Book, by me.")


def test_track_science():
    from r2t2 import track_science, bibliography

    fun_with_reference()
    assert "My Awesome Book, by me." not in bibliography

    track_science()
    fun_with_reference()
    assert "My Awesome Book, by me." in bibliography


def test_print_references(capsys):
    from r2t2 import track_science, print_references

    track_science()
    fun_with_reference()
    print_references()
    captured = capsys.readouterr()

    assert "[1] doing something smart - fun_with_reference()" in captured.out
