import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SignUserServices } from '../../core/api-services/sign-user-services.service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.scss'
})
export class SignUpComponent {
  userData: any = {
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    is_employee: false,
  };

  constructor(
    private router: Router,
    private signUserServices: SignUserServices,
    ) { }

  onPhoneKeyPress(event: KeyboardEvent) {
    const allowedChars = '0123456789';
    const inputChar = String.fromCharCode(event.charCode);
    if (allowedChars.indexOf(inputChar) === -1) {
      event.preventDefault(); // Prevents input of non-numeric characters
    }
  }

  async registerUser() {
    let data = await this.signUserServices.registerUser(this.userData);

    if (data.error) {
      alert(data.error);
      return;
    }

    this.router.navigate(['/authentication/sign-in']);
  }

  goToLoginPage() {
    this.router.navigate(['/authentication/sign-in']);
  }

}
