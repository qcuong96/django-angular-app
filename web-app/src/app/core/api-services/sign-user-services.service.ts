import { Injectable } from '@angular/core';
import { ApiServicesService } from './api-services.service';


@Injectable({
    providedIn: 'root'
  })
export class SignUserServices {

    constructor(private apiServices: ApiServicesService) {}

    async registerUser(body: any) {
        let response = await this.apiServices.request('POST', '/sign_user/sign-up', body, null);
        let data = await response.json();

        if (response.status === 201) {
            return data
        }

        if (data.detail) {
            return {
                error: data.detail
            };
        }

        let errors = ""
        // error data example : {username: ["This field is required."]}
        for (let key in data) {
            errors += `${key}: ${data[key]}\n`
        }

        return {
            error: errors
        }
    }

    async loginUser(body: any) {
        let response = await this.apiServices.request('POST', '/sign_user/sign-in', body, null);
        let data = await response.json();


        if (response.status === 200) {
            return data
        }

        return {
            error: data.detail
        };
    }

}