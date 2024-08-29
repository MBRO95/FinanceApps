import { HttpClient, HttpHeaders} from '@angular/common/http'
import { Injectable } from '@angular/core'

import { Observable, of } from 'rxjs'
import { catchError, map, tap} from 'rxjs/operators'

import { User } from './models/user'

const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json'})
}

@Injectable({ providedIn: 'root'})
export class UserService{

    private api = 'http://127.0.0.1:5000/user'

    constructor( private http: HttpClient){}

    getUser(): Observable<User[]>
    {
        return this.http.get<User[]>(this.api)
    }

    setName(name){
        let body = JSON.stringify(name)
        console.log(body)
        return this.http.post(this.api, body, httpOptions)
    }

}
