from locust import HttpUser, task, between

class AirportUser(HttpUser):
    host = 'http://localhost:8001'
    wait_time = between(1, 3)

    @task(3)
    def list_airports(self):
        self.client.get('/airports/')

    @task(1)
    def get_airport(self):
        self.client.get('/airports/1')

    @task(1)
    def health_check(self):
        self.client.get('/health')

class ItineraryUser(HttpUser):
    host = 'http://localhost:8002'
    wait_time = between(1, 3)

    @task(3)
    def list_itineraries(self):
        self.client.get('/itineraries/')

    @task(1)
    def health_check(self):
        self.client.get('/health')
