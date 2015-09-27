import requests
import os

def build_ins_json(lat, lon, urange):
#     """takes in area info and returns dictionary for server.py to jsonify for D3 request"""

    return_dict = {}
    insurance_providers = []
    # insurance_prov_dict = {}
    docs_by_rating = []

    docs_dict = query_for_doctors(lat, lon, urange)
    
    return_dict["name"] = "area info"
    return_dict["children"] = insurance_providers

    for key, value in docs_dict.items():
        insurance_providers.append({"name": key, "size": value, "children": []})
        # insurance_prov_dict["children"] = docs_by_rating
    return return_dict

def query_for_doctors(lat, lon, urange):
    """Show Doctor Information filtered by location"""
    query_params = {'user_key': 'd9d6a34e907e4b42e1d4ad7a25f7998e',
                    'location': str(lat)+","+str(lon)+","+str(urange),
                    'skip': '0',
                    'limit': '100'
                    }

    endpoint = 'https://api.betterdoctor.com/2015-01-27/doctors?'
    response = requests.get(endpoint, params=query_params)
    print response.json()
    doctors = response.json()['data']

    # ins_dict = query_for_insurance()

    doc_dict = {}

    for doctor in doctors:

        first_name = doctor.get('profile').get('first_name')
        last_name = doctor.get('profile').get('last_name')
        title = doctor.get('profile').get('title')
        gender = doctor.get('profile').get('gender')
        # ratings = doctor.get('ratings')[0].get('rating')
        #returns list
        specialties = doctor.get('specialties')[0].get('name')

        practice = doctor.get('practices')[0].get('name')
        #returns list
        insurance_ids = doctor.get('practices')[0].get('insurance_uids')
        zipcode = doctor.get('practices')[0].get('visit_address').get('zip')

        for i in insurance_ids:
            # name = ins_dict.get(i)
            doc_dict.setdefault(i, 0)
            doc_dict[i] += 1

    return doc_dict

def query_for_insurance():
    """Show Insurance Information"""
    r_insurance = requests.get("https://api.betterdoctor.com/2015-01-27/insurances").json()
    num_pages = r_insurance['last_page']

    query_params = {'apikey': '###'}
    endpoint = 'https://api.betterdoctor.com/2015-01-27/insurances?&user_key=d9d6a34e907e4b42e1d4ad7a25f7998e'
    response = requests.get(endpoint, params=query_params)
    insurance_plans = response.json()['data']

    insurances = {}

    for insurance in insurance_plans:
        insurance_id = insurance.get('plans')[0].get('uid')
        insurance_name = insurance.get('plans')[0].get('name')
        insurances[insurance_id]=insurance_name

    return insurances

# if __name__ == "__main__":

#     build_ins_json(37.773,-122.413,100)
#     # query_for_doctors()
#     # query_for_insurance()
