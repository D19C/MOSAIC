import { animate, style, transition, trigger } from '@angular/animations';

import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FooterComponent } from './footer/footer.component';
import { HostListener } from '@angular/core';
import { LoginComponent } from './login/login.component';
import { NavbarComponent } from './navbar/navbar.component';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, FooterComponent, NavbarComponent, LoginComponent, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  showFooter: boolean = false;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    const scrollPosition = window.innerHeight + window.pageYOffset;
    const documentHeight = document.documentElement.scrollHeight;

    this.showFooter = documentHeight > 0 && scrollPosition >= documentHeight - 1;
  }
  
}
