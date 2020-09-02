def test_register_writer():
    from r2t2.writers import register_writer, REGISTERED_WRITERS

    @register_writer(name="test")
    def test_writer():
        pass

    assert REGISTERED_WRITERS["test"] is test_writer
