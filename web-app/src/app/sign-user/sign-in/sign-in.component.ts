import { Component } from '@angular/core';
import { SignUserServices } from '../../core/api-services/sign-user-services.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.scss'
})
export class SignInComponent {
  username: string = '';
  password: string = '';

  constructor(
    private router: Router,
    private signUserServices: SignUserServices,
  ) { }

  isFormValid(): boolean {
    return this.username.trim() !== '' && this.password.trim() !== '';
  }

  async login() {
    let body = {
      username: this.username,
      password: this.password
    };

    let data = await this.signUserServices.loginUser(body);
    
    if (data.error) {
      alert(data.error);
      return;
    }

    // Save user_id and token in local storage
    localStorage.setItem('user_id', data.user_id);
    localStorage.setItem('authorizationToken', data.token);

    // Redirect to home page
    window.location.href = '/';
  }

  goToRegister() {
    this.router.navigate(['/authentication/sign-up']);
  }
}
