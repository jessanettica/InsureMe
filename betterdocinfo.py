import requests
import os

def build_ins_json(lat, lon, urange):

    """takes in area info and returns dictionary for server.py to jsonify for D3 request"""
    insurances = query_for_insurance()
    return_dict = {}
    insurance_providers = []
    docs_by_rating = []

    docs_dict = query_for_doctors(lat, lon, urange)
    
    return_dict["name"] = "INSURANCE NEAR YOU"
    return_dict["children"] = insurance_providers

    for key, value in docs_dict.items():
        genders = []
        for jdex, gender_count in enumerate(value[2]):
            if jdex == 0:
                gender_dict = {"name": "male", "size": gender_count}
                genders.append(gender_dict)
            else:
                gender_dict = {"name": "female", "size": gender_count}
                genders.append(gender_dict)

        ratings = []
        for idx, rate in enumerate(value[1]):
            if idx == 0:
                rating_dict = {"name": "no rating", "size": rate, "children": genders}
            else:
                rating_dict = {"name": idx, "size": rate, "children": genders}
            ratings.append(rating_dict)
        insurance_providers.append({"name": insurances.get(key, key), "size": value[0], "children": ratings})
    print return_dict
    return return_dict

def query_for_doctors(lat, lon, urange):
    """Show Doctor Information filtered by location"""
    
    
    doc_dict = {}
    doc_count = 0

    #TODO: put cap on number we query in case we get area that has lots of docs.  Maybe cap at 

    query_params = {'user_key': 'd9d6a34e907e4b42e1d4ad7a25f7998e',
                    'location': str(lat)+","+str(lon)+","+str(urange),
                    'skip': '0',
                    'limit': '1'
                    }

    endpoint = 'https://api.betterdoctor.com/2015-01-27/doctors?'
    response = requests.get(endpoint, params=query_params)
    num_responses = response.json()['meta'].get('total')
    print "Total doctors returned: ", num_responses
    if num_responses > 1000:
        num_responses = 1000
    #TODO: limit number of loops - if num_responses > 1,000 then do 10 requests, 100 at a time. else. just loop through all per below
    for num in range(0, num_responses, 100):
        print "num", num
        query_params = {'user_key': 'd9d6a34e907e4b42e1d4ad7a25f7998e',
                    'location': str(lat)+","+str(lon)+","+str(urange),
                    'skip': str(num),
                    'limit': '100'
                    }

        endpoint = 'https://api.betterdoctor.com/2015-01-27/doctors?'
        response = requests.get(endpoint, params=query_params)

        doctors = response.json()['data']

        for doctor in doctors:
            rating_0 = 0
            rating_1 = 0
            rating_2 = 0
            rating_3 = 0
            rating_4 = 0
            rating_5 = 0

            male = 0 #will be zero indx in sublist
            female = 0 #will be 1 indx in sublist

            first_name = doctor.get('profile').get('first_name')
            last_name = doctor.get('profile').get('last_name')
            title = doctor.get('profile').get('title')
            gender = doctor.get('profile').get('gender')

            if gender == "male":
                male += 1
            if gender == "female":
                female += 1
            
            if doctor.get('ratings'):
                ratings = doctor.get('ratings')[0].get('rating')
                if ratings < 2:
                    rating_1 += 1
                elif ratings < 3:
                    rating_2 += 2
                elif ratings < 4:
                    rating_3 += 1
                elif ratings < 5:
                    rating_4 += 1
                else:
                    rating_5 += 1
            else:
                rating_0 += 1

            specialties = doctor.get('specialties')[0].get('name') #returns list

            practice = doctor.get('practices')[0].get('name')
            
            insurance_ids = doctor.get('practices')[0].get('insurance_uids') #returns list
            zipcode = doctor.get('practices')[0].get('visit_address').get('zip')

            #key: ins. ID; value = [#docs ins covers, [#rating 0, 1, 2, 3 4, 5]]
            for i in insurance_ids:
                doc_dict.setdefault(i, [0, [0, 0, 0, 0, 0, 0], [0, 0]])
                doc_dict[i][0] += 1
                doc_dict[i][1][0] += rating_0
                doc_dict[i][1][1] += rating_1
                doc_dict[i][1][2] += rating_2
                doc_dict[i][1][3] += rating_3
                doc_dict[i][1][4] += rating_4
                doc_dict[i][1][5] += rating_5
                doc_dict[i][2][0] += male
                doc_dict[i][2][1] += female 
            doc_count += 1
    
    # limit_to_end = num_responses%100
    # query_params = {'user_key': 'd9d6a34e907e4b42e1d4ad7a25f7998e',
    #             'location': str(lat)+","+str(lon)+","+str(urange),
    #             'skip': '0',
    #             'limit': str(limit_to_end)
    #             }

    # endpoint = 'https://api.betterdoctor.com/2015-01-27/doctors?'
    # response = requests.get(endpoint, params=query_params)

    # doctors = response.json()['data']

    # for doctor in doctors:

    #     first_name = doctor.get('profile').get('first_name')
    #     last_name = doctor.get('profile').get('last_name')
    #     title = doctor.get('profile').get('title')
    #     gender = doctor.get('profile').get('gender')
    #     # ratings = doctor.get('ratings')[0].get('rating')
        
    #     specialties = doctor.get('specialties')[0].get('name') #returns list

    #     practice = doctor.get('practices')[0].get('name')
        
    #     insurance_ids = doctor.get('practices')[0].get('insurance_uids') #returns list
    #     zipcode = doctor.get('practices')[0].get('visit_address').get('zip')

    #     for i in insurance_ids:
    #         # name = ins_dict.get(i)
    #         doc_dict.setdefault(i, 0)
    #         doc_dict[i] += 1
    #     doc_count += 1

    return doc_dict


def query_for_insurance():
    """Show Insurance Information"""
    insurances = {}
    query_params = {'user_key': 'd9d6a34e907e4b42e1d4ad7a25f7998e',
                    'limit': '1'
                    }

    response = requests.get("https://api.betterdoctor.com/2015-01-27/insurances", params=query_params)
    # response = requests.get(endpoint, params=query_params)
    num_responses = response.json()['meta'].get('total')
    print "number of insurances: ", num_responses

    for num in range(0, num_responses, 100):
        print "num", num
        query_params = {'user_key': 'd9d6a34e907e4b42e1d4ad7a25f7998e',
                    'skip': str(num),
                    'limit': '100'
                    }
        r_insurance = requests.get("https://api.betterdoctor.com/2015-01-27/insurances", params=query_params).json()

        insurance_plans = r_insurance['data']


        for insurance in insurance_plans:
            insurance_id = insurance.get('plans')[0].get('uid')
            insurance_name = insurance.get('plans')[0].get('name')
            insurances[insurance_id]=insurance_name
    print insurances
    return insurances



# if __name__ == "__main__":
    
    # print build_ins_json(47.811436, -112.187988,50)
    # print query_for_doctors(47.811436, -112.187988,50)
    # query_for_insurance()
