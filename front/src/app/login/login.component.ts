import { Component, OnInit } from '@angular/core';

import { AuthService } from '../services/services';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent{
  keep_logged_in: boolean = true;
  user: string = 'admin';
  password: string = 'admin123';
  type: string = 'admin';

  constructor(private authService: AuthService) { }

  login() {
    this.authService.authenticate(this.user, this.password, this.type, this.keep_logged_in)
      .subscribe(
        response => {
          // Manejar la respuesta exitosa de la autenticación aquí
          console.log('Autenticación exitosa:', response);
        },
        error => {
          // Manejar cualquier error de la autenticación aquí
          console.error('Error en la autenticación:', error);
        }
      );
  }
}
