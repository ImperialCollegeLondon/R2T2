from r2t2 import add_reference, BIBLIOGRAPHY

@add_reference(short_purpose="Demonstrate class reference",
                   reference="A reference for a class")
class MyGreatClass():

    @add_reference(short_purpose="Demonstrate class method reference",
                   reference="A reference for a class method")
    def my_great_class_method(self):
        pass

if __name__ == "__main__":
    BIBLIOGRAPHY.tracking()
    my_class = MyGreatClass()
    print(BIBLIOGRAPHY)