import requests
import json
import time

bearer_token = "fjqzesvsdwsaggfvd3wkfw3j"
authorization = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjcxODM4MTAsImlzcyI6IkdBUEkiLCJ0b2tlbl90eXBlIjoic3RhbmRhcmQiLCJ1c2VybmFtZSI6Ijg0MzQ0NjMwMjIiLCJmdWxsX25hbWUiOiJKT1NFUEggV0VJU1MifQ.yenVffNuQKpDAXDwtf_ZFi2xuE_pUa85X-ohTmUYRPQ"

filename = 'cars.csv'
f = open(filename, 'w+')

headers = "Year, Make, Model, Style, Price \n"
f.write(headers)

for year in range(2013, 2016):

    
    burp0_url = "https://gapiprod.awsmlogic.manheim.com:443/gateway"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Authorization": authorization, "X-Mmr-Version": "sha: d6ba5531f7025bdc3437023648cfa29fbbc00f16, type: application", "X-Velocity-Tracer": "", "Content-Type": "application/json", "Origin": "https://mmr.manheim.com", "Referer": "https://mmr.manheim.com/?WT.svl=m_uni_hdr_buy&country=US&popup=true&source=man", "Te": "trailers"}
    burp0_json={"requests": [{"bearer_token": bearer_token, "href": "https://webservices.manheim.com/MMRDecoderWebService/decoders/makeList?year=" + str(year) + "&country=US"}]}
    time.sleep(0.125)
    response = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
    resp_dict = json.loads(response.text)
    try:
        makes = resp_dict['responses'][0]['body']['make']
    except KeyError as e:
        print("I got a keyerror... here's json " + str(resp_dict))
        continue

    for make in makes:

        burp0_url = "https://gapiprod.awsmlogic.manheim.com:443/gateway"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Authorization": authorization, "X-Mmr-Version": "sha: d6ba5531f7025bdc3437023648cfa29fbbc00f16, type: application", "X-Velocity-Tracer": "", "Content-Type": "application/json", "Origin": "https://mmr.manheim.com", "Referer": "https://mmr.manheim.com/?WT.svl=m_uni_hdr_buy&country=US&popup=true&source=man", "Te": "trailers"}
        burp0_json={"requests": [{"bearer_token": bearer_token, "href": "https://webservices.manheim.com/MMRDecoderWebService/decoders/modelList/make/" + str(make['id']) + "?year=" + str(year) + "&country=US"}]}
        time.sleep(0.25)
        response = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)

        resp_dict = json.loads(response.text)
        try:
            models = resp_dict['responses'][0]['body']['model']
        except KeyError as e:
                    print("I got a keyerror... here's json " + str(resp_dict))
        
        
        for model in models:

            burp0_url = "https://gapiprod.awsmlogic.manheim.com:443/gateway"
            burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Authorization": authorization, "X-Mmr-Version": "sha: d6ba5531f7025bdc3437023648cfa29fbbc00f16, type: application", "X-Velocity-Tracer": "", "Content-Type": "application/json", "Origin": "https://mmr.manheim.com", "Referer": "https://mmr.manheim.com/?WT.svl=m_uni_hdr_buy&country=US&popup=true&source=man", "Te": "trailers"}
            burp0_json={"requests": [{"bearer_token": bearer_token, "href": "https://webservices.manheim.com/MMRDecoderWebService/decoders/styleList/make/" + str(make['id']) + "/model/" + str(model['id']) + "/year/" + str(year) + "?country=US"}]}
            response = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)

            resp_dict = json.loads(response.text)
            try:
                styles = resp_dict['responses'][0]['body']['style']
            except KeyError as e:
                    print("I got a keyerror... here's json " + str(resp_dict))

            #print(response.status_code)
            
            

            for style in styles:
                #print(str(make['name']) + " " + str(model['name']) + " " + str(style['name']))

                burp0_url = "https://gapiprod.awsmlogic.manheim.com:443/gateway"
                burp0_headers = {
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
                        "Accept": "*/*",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate",
                        "Authorization": authorization,
                        "X-Mmr-Version": "sha: d6ba5531f7025bdc3437023648cfa29fbbc00f16, type: application",
                        "X-Velocity-Tracer": "",
                        "Content-Type": "application/json",
                        "Origin": "https://mmr.manheim.com",
                        "Referer": "https://mmr.manheim.com/?WT.svl=m_uni_hdr_buy&country=US&popup=true&source=man",
                        "Te": "trailers"
                        }                
                burp0_json={"requests": [{"bearer_token": bearer_token, "href": "https://api.manheim.com/valuations/id/"+ str(year) + str(make['id']) + str(model['id']) + str(style['id']) +"?country=US&region=NA&include=retail,historical,forecast&orgId="}, {"bearer_token": bearer_token, "href": "https://api.manheim.com/valuation-samples/id/" + str(year) + str(make['id']) + str(model['id']) + str(style['id']) + "?country=US&orderBy=purchaseDate desc&start=1&limit=100"}]}
                response = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)

                resp_dict = json.loads(response.text)
                
                try:
                    print(str(year) + " " + str(make['name']) + " " + str(model['name']) + " " + str(style['name']) + " " + str(resp_dict['responses'][0]['body']['items'][0]['adjustedPricing']['wholesale']['average']))
                except KeyError as e:
                    print("I got a keyerror... here's json " + str(resp_dict))
                time.sleep(0.33)
                try:
                    f.write(str(year) + "," + str(make['name']) + "," + str(model['name']) + "," + str(style['name']) + "," + str(resp_dict['responses'][0]['body']['items'][0]['adjustedPricing']['wholesale']['average']) + "\n")
                except KeyError as e:
                    print("I got a keyerror... here's json " + str(resp_dict))
 
f.close()
