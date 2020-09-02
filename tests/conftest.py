from pytest import fixture


@fixture
def decorated_function():
    from r2t2 import add_reference

    @add_reference(
        short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
    )
    def roasted_chicken(ingredients=None):
        pass

    return roasted_chicken


@fixture
def decorated_with_doi():
    from r2t2 import add_reference

    @add_reference(short_purpose="DOI reference", doi="10.5281/zenodo.1185316")
    def a_great_function():
        pass

    return a_great_function
