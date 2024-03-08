import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { CentroComponent } from './centro/centro.component';
import { LoginComponent } from './login/login.component';
import { NgModule } from '@angular/core';
import { SignupComponent } from './signup/signup.component';

const routes: Routes = [
  { path: '', component: CentroComponent},
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  // Otras rutas aquí...
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
