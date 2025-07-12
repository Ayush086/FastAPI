### WHY THEIR IS A NEED FOR PYDANTIC ?                                                                                                   09/07/2025

# type hinting doesn't produce error eg. input -> 'ayush', '40' will get executed successfully
def insert_patient_data(name: str, age: int):
    print(name, " ", age)
    print("entry inserted in DB")

# another approch for data validation will explicitly checking datatypes using conditional statements
def insert_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        print(name, " ", age)
        print("entry inserted in DB")
    else: 
        raise TypeError("Incorrect DataType")
    
# but the above method isn't scalable, need to write extra code for every functions where arguments are needed.
# will need to write additional code for data validation separately.


