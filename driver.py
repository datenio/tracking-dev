import redis

r = redis.Redis(host="127.0.0.1", port="6379", password="")


class DriversPool:
    def __init__(self):
        drivers = {}
        for driver in r.keys("driver-*"):
            path = []
            i = 1
            none_pos = False
            while not none_pos:
                i += 1
                pos = r.geopos(driver, i)
                if pos == [None]:
                    none_pos = True
                    drivers[driver.decode("utf-8")] = len(path)
                else:
                    path.append(pos)

        print(f"{drivers}")
        self.drivers = drivers

    def add_driver(self, identifier, initial_lat, initial_lon):

        r.geoadd("driver-" + identifier, initial_lat, initial_lon, 1)
        self.drivers["driver-" + identifier] = 1

    # def initiate_index_saved(self):
    #     for i i

    def get_last_index(self, identifier):
        index = self.drivers["driver-" + identifier]
        return index

    def update_pos(self, identifier, lat, lon):
        self.drivers["driver-" + identifier] += 1

        index = self.drivers["driver-" + identifier]
        r.geoadd("driver-" + identifier, lat, lon, index)

    def driver_in_pool(self, identifier):
        return ("driver-" + identifier) in self.drivers

    def get_all_drivers(self):
        return list(self.drivers.keys())

    def get_path(self, identifier):

        path = []

        index = self.drivers["driver-" + identifier]

        for i in range(1, index + 1):
            path.append(r.geopos("driver-" + identifier, i))

        return path


pool = DriversPool()

print(pool.get_last_index("1"))
# pool.add_driver("1", 1.1, 2.2)
# pool.add_driver("2", 1.1, 2.2)
# pool.add_driver("3", 1.1, 2.2)

# if(pool.driver_in_pool("3")):
#     pool.update_pos("3", 1.1, 3.3)
#     pool.update_pos("1", 1.1, 3.3)
#     pool.update_pos("1", 1.1, 3.3)
# else:
#     pool.add_driver("3", 2.2, 3.3)


# print(pool.get_all_drivers())
# r.geoadd("identifier", 1.11, 2.222, 1)
# r.geoadd("identifier", 3.333, lon, 2)


## TO - DO 

## cuando socket haga un cambio, hacer un update
## AL HACER UN UPDATE CON ID, socket al ultimo dato 
