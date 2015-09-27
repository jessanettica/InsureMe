import requests
import os


def query_for_doctors():
    """Show Doctor Information filtered by location"""
    query_params = {'apikey': '###'}
    endpoint = 'https://api.betterdoctor.com/2015-01-27/doctors?location=37.773%2C-122.413%2C100&user_location=37.773%2C-122.413&skip=0&limit=2&user_key=d9d6a34e907e4b42e1d4ad7a25f7998e'
    response = requests.get(endpoint, params=query_params)
    doctors = response.json()['data']

    for doctor in doctors:

        first_name = doctor.get('profile').get('first_name')
        last_name = doctor.get('profile').get('last_name')
        title = doctor.get('profile').get('title')
        gender = doctor.get('profile').get('gender')
        ratings = doctor.get('ratings')[0].get('rating')
        specialties = doctor.get('specialties')[0].get('name')

        practice = doctor.get('practices')[0].get('name')
        insurance_id = doctor.get('practices')[0].get('insurance_uids')
        zipcode = doctor.get('practices')[0].get('visit_address').get('zip')

    return

def query_for_insurance():
    """Show Insurance Information"""
    query_params = {'apikey': '###'}
    endpoint = 'https://api.betterdoctor.com/2015-01-27/insurances?skip=0&limit=10&user_key=d9d6a34e907e4b42e1d4ad7a25f7998e'
    response = requests.get(endpoint, params=query_params)
    insurance_plans = response.json()['data']

    for insurance in insurance_plans:
        insurance_id = insurance.get('plans')[0].get('uid')
        insurance_name = insurance.get('plans')[0].get('name')
        insurances[insurance_id]=insurance_name
    return insurances

if __name__ == "__main__":

    query_for_doctors()
    query_for_insurance()
