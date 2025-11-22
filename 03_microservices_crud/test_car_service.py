# from shemas import CarCreate, CarUpdate
# from services.car_service import CarService



# def test_create_car():
#     car_service = CarService()
#     car = car_service.create(CarCreate(make="Toyota", model="Corolla", year=2020))


#     assert car.id == 1
#     assert car.make == "Toyota"
#     assert car.model == "Corolla"


# def test_list_all_cars():
#     car_service = CarService()
#     car_service.create(CarCreate(make="Honda", model="Civic", year=2019))
#     car_service.create(CarCreate(make="Ford", model="Focus", year=2018))

#     all_cars = car_service.list_all()

#     assert len(all_cars) == 2
#     assert all_cars[0].make == "Honda"
#     assert all_cars[1].make == "Ford"

# def test_get_car():
#     car_service = CarService()
#     res = car_service.get(999)

#     assert res is None

# def test_update_car():
#     car_service = CarService()

#     car = car_service.create(CarCreate(make="Nissan", model="Altima", year=2017))

#     updated_car = car_service.update(car.id, CarUpdate(model="Sentra"))

#     assert updated_car is not None
#     assert updated_car.id == car.id
#     assert updated_car.model == "Sentra"
#     assert updated_car.year == 2017


# def test_update_car_not_found():
#     car_service = CarService()
#     result = car_service.update(999, CarUpdate(model="Sentra"))

#     assert result is None


# def test_delete_car():
#     car_service = CarService()

#     car = car_service.create(CarCreate(make="Chevrolet", model="Malibu", year=2016))

#     ok = car_service.delete(car.id)

#     assert ok is True
#     assert len(car_service.list_all()) == 0




# def test_delete_car_not_found():
#     car_service = CarService()
#     ok = car_service.delete(999)

#     assert ok is False