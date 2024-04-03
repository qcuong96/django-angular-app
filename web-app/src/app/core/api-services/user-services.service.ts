import { Injectable } from '@angular/core';
import { ApiServicesService } from './api-services.service';


@Injectable({
    providedIn: 'root'
  })
export class UserServices {

    constructor(private apiServices: ApiServicesService) {
        this.apiServices.addOrUpdateHeaders('Authorization', localStorage.getItem('authorizationToken'));
    }

    async getUserDetail() {
        let response = await this.apiServices.request('GET', '/user/' + localStorage.getItem("user_id"), null, null);
        let data = await response.json();

        if (response.status === 200) {
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

}