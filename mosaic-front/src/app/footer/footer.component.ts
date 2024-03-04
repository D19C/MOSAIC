import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { HostListener } from '@angular/core';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css'
})
export class FooterComponent {
  showFooter: boolean = true;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    const scrollPosition = window.innerHeight + window.pageYOffset;
    const mainContentHeight = document.querySelector('.welcome-container')?.scrollHeight;

    if (mainContentHeight !== undefined) {
      // Mostrar el footer cuando se llegue al final del contenido principal
      this.showFooter = scrollPosition >= mainContentHeight;
      console.log("hola", this.showFooter);
    }
  }
}
