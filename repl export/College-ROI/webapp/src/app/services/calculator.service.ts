import { HttpClient, HttpHeaders} from '@angular/common/http'
import { Injectable } from '@angular/core'

import { Observable, of } from 'rxjs'
import { catchError, map, tap} from 'rxjs/operators'
import { ChartDataSets, ChartOptions } from 'chart.js';


import { College } from './models/college'
import { Resolve, ActivatedRouteSnapshot } from "@angular/router";
import { RouterStateSnapshot } from "@angular/router";

const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json'})
}

@Injectable({ providedIn: 'root'})
export class CalculatorService implements Resolve<any>{

    constructor( private http: HttpClient ){}

    addPrinciple(principle){
        let body = JSON.stringify(principle)
        console.log(body)
        return this.http.post('http://127.0.0.1:5000/principle', body, httpOptions)
    }

    updateRepaymentPercentage(repayment){
        console.log(repayment)
        let body = JSON.stringify(repayment)
        return this.http.post('http://127.0.0.1:5000/repayment', body, httpOptions)
    }

    setAge(age){
        let body = JSON.stringify(age)
        console.log(body)
        return this.http.post('http://127.0.0.1:5000/age', body, httpOptions)
    }

    setIsInState(isInState){
        let body = JSON.stringify(isInState)
        console.log(body)
        return this.http.post('http://127.0.0.1:5000/tuition', body, httpOptions)
    }

    //getLineChartData()
    resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<ChartDataSets[]>
    {
        return this.http.get<ChartDataSets[]>('http://127.0.0.1:5000/chartdata')
    }

    getLineChartData(){
        return this.http.get<ChartDataSets[]>('http://127.0.0.1:5000/chartdata')
    }


}
