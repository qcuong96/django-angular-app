import * as qs from 'qs';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ApiServicesService {
  baseApiUrl: string;
  headers: any = {
    'Content-Type': 'application/json',
  };

  constructor() { 
    this.baseApiUrl = environment.baseApiUrl + '/api/' + environment.apiVersion;
  }

  private generateQueryString(params: any) {
    return params ? `?${qs.stringify(params)}` : ''
  }

  addOrUpdateHeaders(header_name: string, header_value: any) {
    this.headers[header_name] = header_value;
  }

  remove_header(header_name: string) {
    delete this.headers[header_name];
  }

  async request(method: string, endpoint: string, body: any, params: any) {
    const url = this.baseApiUrl + endpoint + this.generateQueryString(params);
    let options = {
      method,
      headers: this.headers,
      body: body ? JSON.stringify(body) : null,
    };

    return fetch(url, options);
  }
}