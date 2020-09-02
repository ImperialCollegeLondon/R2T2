from r2t2 import add_reference, BIBLIOGRAPHY


@add_reference(
    short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
)
def roasted_chicken(ingredients=None):
    pass


# BIBLIOGRAPHY.tracking()
roasted_chicken()
print(BIBLIOGRAPHY)
