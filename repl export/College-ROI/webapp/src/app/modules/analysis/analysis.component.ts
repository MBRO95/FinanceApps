import { Component, OnInit, OnChanges, AfterViewInit } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';

import { CalculatorService } from '@app/services/calculator.service'
import { of, Observable} from "rxjs";
import { share } from "rxjs/internal/operators/share";
import { ActivatedRoute } from "@angular/router";
import { map } from 'rxjs/operators';
import { UserService } from "@app/services/user.service";
import { User } from "@app/services/models/user";
import { MatSnackBar, MAT_SNACK_BAR_DATA } from '@angular/material/snack-bar'
import { RatingbarComponent} from '@app/components'

@Component({
  selector: 'exemplar-analysis',
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.scss'],
  providers: [CalculatorService]
})

export class AnalysisComponent implements OnInit, AfterViewInit{

  autoTicks = false;
  disabled = false;
  invert = false;
  max = 100;
  min = 0;
  showTicks = false;
  step = 1;
  thumbLabel = true;
  value = 20;
  vertical = false;

  userCollege: String
  userDegree: String
  userName: String
  totalCost: string
  startingSalary: String
  midSalary: String
  roi: number
  age: string
  lifetimeEarnings: string
  debtRepaymentAge: string

  lineChartData: ChartDataSets[] = [];

  constructor(
    private actr: ActivatedRoute, 
    private _calculatorService: CalculatorService, 
    private _userService: UserService, 
    private _snackBar: MatSnackBar,
    
  ) {}

  ngAfterViewInit(){
    setTimeout( ()=>{
      this.openSnackBar()
      }, 10000)
  }

  durationInSeconds = 5;
  openSnackBar() {
    this._snackBar.openFromComponent(RatingbarComponent, {
      duration: 500000,
    })
  }

  ngOnInit() {
    let yearly_earnings_data = JSON.parse(this.actr.snapshot.data.cres['yearly_earnings'])
    let cumulative_earnings_data = JSON.parse(this.actr.snapshot.data.cres['cumulative_earnings'])
    let repayment_data = JSON.parse(this.actr.snapshot.data.cres['repayment'])
    let hs_data = JSON.parse(this.actr.snapshot.data.cres['hs_earnings'])
    let cumulative_hs = JSON.parse(this.actr.snapshot.data.cres['cumulative_hs'])
    
    this.userCollege = this.actr.snapshot.data.cres['college']
    this.userDegree = this.actr.snapshot.data.cres['degree'] 
    this.userName = this.actr.snapshot.data.cres['name']
    this.totalCost = this.actr.snapshot.data.cres['total_cost'].substring(1)
    this.startingSalary = this.actr.snapshot.data.cres['starting_salary']
    this.midSalary = this.actr.snapshot.data.cres['mid_salary']
    this.age = this.actr.snapshot.data.cres['age']
    this.roi = Math.round((cumulative_earnings_data[cumulative_earnings_data.length - 1] - parseFloat(this.totalCost)) / parseFloat(this.totalCost))
    this.lifetimeEarnings = cumulative_earnings_data[cumulative_earnings_data.length - 1]
    this.debtRepaymentAge = repayment_data.findIndex(this.getRepaymentIndex) + this.age
    this.value = this.actr.snapshot.data.cres['repayment_percent']

    this.lineChartData.push({ data: yearly_earnings_data, label: 'Salary Year Over Year'})
    this.lineChartData.push({ data: cumulative_earnings_data, label: 'Cumulative Lifetime Earnings'})
    this.lineChartData.push({ data: cumulative_hs, label: 'Highschool Grad Cumulative Earnings'})
    this.lineChartData.push({ data: hs_data, label: "Highschool Earnings"})
    this.lineChartData.push({ data: repayment_data, label: 'Repayment Timeline'})

  }

  getRepaymentIndex(element){
    return element == 0
  }

  updateRepaymentAge($event){
    this.debtRepaymentAge = $event
  }

  updateRepaymentPercent(repayment){
    let amount = {repayment: repayment}
    this._calculatorService.updateRepaymentPercentage(amount).subscribe()
    const calcObservable = this._calculatorService.getLineChartData()

    calcObservable.subscribe((data: any[]) => {
      this.lineChartData[4]={ data: data['repayment'], label: 'Repayment Timeline'}
    })
  }

}
