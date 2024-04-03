import { Component, OnInit } from '@angular/core';
import { UserServices } from '../../core/api-services/user-services.service';

@Component({
  selector: 'app-side-navbar',
  templateUrl: './side-navbar.component.html',
  styleUrl: './side-navbar.component.scss'
})
export class SideNavbarComponent implements OnInit{
  username: any = '';
  
  constructor(
    private userServices: UserServices,
  ) {
  }

  async ngOnInit() {
    let data = await this.userServices.getUserDetail();
    if (data.error) {
      alert(data.error);
      return;
    }

    this.username = data.username;
    localStorage.setItem('username', data.username);
    localStorage.setItem('is_employee', data.is_employee);
  }

  logout() {
    // clear all local storage
    localStorage.clear();
    
    // reload the page
    window.location.reload();
  }

}
