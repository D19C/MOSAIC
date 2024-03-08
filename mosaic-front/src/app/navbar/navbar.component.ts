import { Router, RouterOutlet } from '@angular/router';

import { Component } from '@angular/core';
import { LoginComponent } from '../login/login.component';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [LoginComponent, RouterOutlet, RouterModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  constructor(private router: Router) { }
  navigateToLogin() {
    this.router.navigateByUrl('/login');
  }

  navigateToSignup() {
    this.router.navigateByUrl('/signup');
  }
  
}
