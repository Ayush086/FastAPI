from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pincode: str
    
class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address
    
address_dict = {'city': "pune", 'state': 'maharashtra', 'pincode': '411048'}

address1 = Address(**address_dict)

p1_dict = {'name': 'ayush', 'gender': 'male', 'age': 22, 'address': address1}

p1 = Patient(**p1_dict)

print(p1)

# exporting to python dict
# temp = p1.model_dump
# print(temp)
# print(type(temp))

# exporting to json
t = p1.model_dump_json
print(t)
print(type(t))