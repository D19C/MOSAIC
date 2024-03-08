import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  authenticate(
    keep_logged_in: boolean = true,
    type: string,
    user: string,
    password: string) {
    const url = 'http://127.0.0.1:8000/base/auth';
    const body = { 
        keep_logged_in: true,
        password: password,
        user: user,
        type: type
    };

    // Define los encabezados
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      // Otros encabezados si es necesario
    });

    // Realiza la solicitud HTTP con los encabezados
    return this.http.post(url, body, { headers: headers });
  }
}
