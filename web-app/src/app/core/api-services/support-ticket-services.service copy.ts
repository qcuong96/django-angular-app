import { Injectable } from '@angular/core';
import { ApiServicesService } from './api-services.service';


@Injectable({
    providedIn: 'root'
})
export class SupportTicketServices {

    constructor(private apiServices: ApiServicesService) {
        this.apiServices.addOrUpdateHeaders('Authorization', localStorage.getItem('authorizationToken'));
    }

    async getListSupportTicket(page = 1) {
        let response = await this.apiServices.request('GET', '/support_ticket', null, { page: page });
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

    async createSupportTicket(body: any) {
        let response = await this.apiServices.request('POST', '/support_ticket', body, null);
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

    async getDetailSupportTicket(support_ticket_id: string) {
        let response = await this.apiServices.request('GET', '/support_ticket/' + support_ticket_id, null, null);
        let data = await response.json();


        if (response.status === 200) {
            let _result = {
                name: data.name,
                description: data.description,
                priority: data.priority,
                category: data.category,
                status: data.status,
                create_time: data.create_time,
                update_time: data.update_time,
                supporter: data.supporter,
                reporter: data.reporter,
                replies: []
            }

            let replies_response = await this.apiServices.request('GET', '/support_ticket/' + support_ticket_id + '/reply', null, null);
            let replies_data = await replies_response.json();

            if (replies_response.status === 200) {
                _result.replies = replies_data
                return _result
            }

            if (replies_data.detail) {
                return {
                    error: replies_data.detail
                };
            }

            let errors = ""
            // error data example : {username: ["This field is required."]}
            for (let key in replies_data) {
                errors += `${key}: ${replies_data[key]}\n`
            }

            return {
                error: errors
            }
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

    async createReply(support_ticket_id: string, body: any) {
        let response = await this.apiServices.request('POST', '/support_ticket/' + support_ticket_id + '/reply', body, null);
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

    async closeSupportTicket(support_ticket_id: string) {
        let response = await this.apiServices.request('PUT', '/support_ticket/' + support_ticket_id + '/close', null, null);
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

    async assignSupporter(support_ticket_id: string, user_id: string) {
        let response = await this.apiServices.request('PUT', '/support_ticket/' + support_ticket_id + '/assign', null, {user_id: user_id});
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

    async deleteSupportTicket(support_ticket_id: string) {
        let response = await this.apiServices.request('DELETE', '/support_ticket/' + support_ticket_id, null, null);
        let data = await response.json();

        if (response.status === 204) {
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