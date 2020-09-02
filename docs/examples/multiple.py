from r2t2 import add_reference


@add_reference(short_purpose="some comment", reference="Reference 1")
@add_reference(short_purpose="another comment", reference="Reference 2")
def my_great_function():
    pass
