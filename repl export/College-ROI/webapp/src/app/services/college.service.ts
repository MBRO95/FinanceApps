import { HttpClient, HttpHeaders} from '@angular/common/http'
import { Injectable } from '@angular/core'

import { Observable, of } from 'rxjs'
import { catchError, map, tap} from 'rxjs/operators'

import { College } from './models/college'

const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json'})
}

@Injectable({ providedIn: 'root'})
export class CollegeService{

    private collegeUrl = 'http://127.0.0.1:5000/colleges' //url to web api

    constructor( private http: HttpClient){}

    getColleges(): Observable<College[]>
    {
        return this.http.get<College[]>(this.collegeUrl)
    }

    getCollegesByAbbr(state: String): Observable<College[]>
    {
        return this.http.get<College[]>(this.collegeUrl + '/' + state)
    }

    setCollege(college){
        let body = JSON.stringify(college)
        console.log(body)
        return this.http.post(this.collegeUrl, body, httpOptions)
    }

}
